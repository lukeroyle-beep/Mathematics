#!/usr/bin/env python3
"""Build, validate, run and resume the independent exact Stage 4 search."""
import argparse
import fcntl
import hashlib
import itertools
import json
import math
import os
from pathlib import Path
import platform
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from functools import lru_cache

HERE = Path(__file__).resolve().parent
BUILD = Path(os.environ.get("A398769_BUILD", "/private/tmp/a398769-stage4-build"))
SCHEMA = 1
if not __debug__:
    raise RuntimeError("Run without -O: validation assertions must stay enabled")


def now():
    return datetime.now(timezone.utc).isoformat()


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_id():
    h = hashlib.sha256()
    for name in ("search.cpp", "search.py"):
        h.update(name.encode() + b"\0" + (HERE / name).read_bytes())
    return h.hexdigest()


def atomic_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp = tempfile.mkstemp(prefix=path.name + ".", dir=path.parent)
    try:
        with os.fdopen(fd, "w") as out:
            json.dump(data, out, indent=2, sort_keys=True)
            out.write("\n")
            out.flush()
            os.fsync(out.fileno())
        os.replace(temp, path)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)


def build():
    BUILD.mkdir(parents=True, exist_ok=True)
    compiler = os.environ.get("CXX", "c++")
    gmp = os.environ.get("GMP_PREFIX", "/opt/homebrew")
    command = [compiler, "-O3", "-std=c++17", "-Wall", "-Wextra", "-Werror",
               "-isystem", gmp + "/include", "-L" + gmp + "/lib",
               str(HERE / "search.cpp"), "-lgmpxx", "-lgmp", "-o", str(BUILD / "search")]
    subprocess.run(command, check=True)
    meta = {"source_sha256": source_id(), "binary_sha256": digest(BUILD / "search"),
            "compiler": subprocess.check_output([compiler, "--version"], text=True).strip(),
            "command": command, "platform": platform.platform(), "machine": platform.machine(),
            "built_at": now()}
    atomic_json(BUILD / "build.json", meta)
    return meta


def ensure_build():
    try:
        meta = json.loads((BUILD / "build.json").read_text())
        if (meta["source_sha256"] == source_id()
                and meta["binary_sha256"] == digest(BUILD / "search")):
            return meta
    except (OSError, KeyError, ValueError):
        pass
    return build()


def engine(length, b, divisor, seconds=0, max_nodes=0):
    command = [str(BUILD / "search"), str(length), str(b), str(divisor),
               str(max_nodes), str(max(1, int(seconds * 1000)) if seconds else 0)]
    result = subprocess.run(command, check=True, text=True, capture_output=True,
                            timeout=seconds + 30 if seconds else None)
    record = json.loads(result.stdout)
    assert record["length"] == length and record["b"] == b
    assert record["divisor"] == str(divisor)
    assert record["status"] in ("complete", "limited")
    assert len(record["witnesses"]) == len(set(record["witnesses"]))
    expected_nodes, expected_leaves = work_bound(length, b, divisor)
    record["expected_complete_nodes"] = expected_nodes
    record["expected_complete_leaves"] = expected_leaves
    assert record["nodes"] <= expected_nodes and record["leaves"] <= expected_leaves
    if record["status"] == "complete":
        assert record["termination_reason"] == "exhausted"
        assert record["nodes"] == expected_nodes and record["leaves"] == expected_leaves
    for m in record["witnesses"]:
        assert len(m) == length and set(m) <= {"1", "3"} and m.count("3") == b
        assert int(m) % divisor == 0
    return record


def work_bound(length, b, divisor):
    """Exact size of the finite traversal tree, computed without searching it."""
    repunits = [(10 ** r - 1) // 9 for r in range(length + 1)]

    @lru_cache(None)
    def size(r, k):
        if 2 * repunits[k] * (10 ** (r - k) - 1) < 2 * divisor:
            return 1, 1
        children = []
        if k < r:
            children.append(size(r - 1, k))
        if k:
            children.append(size(r - 1, k - 1))
        return 1 + sum(c[0] for c in children), sum(c[1] for c in children)

    return size(length, b)


def parameters(length, b):
    assert 1 <= length <= 75 and 0 <= b <= length
    t = length + 2 * b
    divisor = 3 ** (length + b) * t
    # Order matters only for the label. Every reason is independently necessary.
    if length % 2 == 0:
        reason = "even_length"
    elif (length + b >= 2 and t % 9 != 0) or (length + b == 1 and t % 3 != 0):
        reason = "digit_sum_mod_9_or_3"
    elif t % 5 == 0:
        reason = "factor_5"
    elif divisor > int("3" * b + "1" * (length - b)):
        reason = "divisor_above_maximum"
    else:
        reason = None
    return divisor, reason


def verify_original(n, length=None, b=None):
    s = str(n)
    assert n > 0 and set(s) <= {"3", "9"}
    if length is not None:
        assert len(s) == length and s.count("9") == b
    p = math.prod(map(int, s))
    total = sum(map(int, s))
    q, remainder = divmod(n, p * total)
    assert remainder == 0
    return {"n": str(n), "digit_product": str(p), "digit_sum": total,
            "quotient": str(q)}


def validate():
    meta = ensure_build()
    start = time.monotonic()
    originals = 0
    tested_cases = 0
    # Independent oracle: actual n digits, no reduced formula or exclusion rules.
    for length in range(1, 17):
        expected = {b: [] for b in range(length + 1)}
        for digits in itertools.product((3, 9), repeat=length):
            n = int("".join(map(str, digits)))
            originals += 1
            if n % (math.prod(digits) * sum(digits)) == 0:
                expected[digits.count(9)].append(str(n // 3))
        for b in range(length + 1):
            divisor, excluded = parameters(length, b)
            if divisor % 2 == 0:
                assert excluded == "even_length" and not expected[b]
                continue
            # Exercise the actual engine even on cases the production driver excludes.
            actual = engine(length, b, divisor)
            assert actual["status"] == "complete"
            assert sorted(actual["witnesses"]) == sorted(expected[b]), (length, b)
            assert not excluded or not expected[b]
            tested_cases += 1
    # Generic nonzero tests use the same engine and independently enumerated words.
    control_cases = 0
    control_hits = 0
    for length in range(1, 9):
        words = ["".join(d) for d in itertools.product("13", repeat=length)]
        for divisor in (1, 9, 17, 101):
            for b in range(length + 1):
                expected = sorted(w for w in words if w.count("3") == b and int(w) % divisor == 0)
                actual = engine(length, b, divisor)
                assert actual["status"] == "complete"
                assert sorted(actual["witnesses"]) == expected, (length, b, divisor)
                control_hits += len(expected)
                control_cases += 1
    known = ["111133131", "111331113", "113131311", "133113111", "311113311"]
    assert engine(9, 3, 17)["witnesses"] == known
    assert control_hits > 0
    # 75-digit arithmetic and nonempty terminal intervals, checked by enumeration
    # of the 75 possible positions, not by the search's own prefix recursion.
    for divisor in (1, 17, 3 ** 80 + 2):
        words = ["1" * i + "3" + "1" * (74 - i) for i in range(75)]
        expected = sorted(w for w in words if int(w) % divisor == 0)
        actual = engine(75, 1, divisor)
        assert actual["status"] == "complete" and sorted(actual["witnesses"]) == expected
    limited = engine(20, 10, 1, max_nodes=3)
    assert limited["status"] == "limited"
    timed = engine(75, 12, parameters(75, 12)[0], seconds=0.001)
    assert timed["status"] == "limited" and timed["termination_reason"] == "time_limit"
    assert [b for b in range(76) if parameters(75, b)[1] is None] == [3, 12, 21, 39, 48, 57, 66]
    report = {"status": "passed", "source_sha256": source_id(), "build": meta,
              "original_condition_words": originals, "original_condition_max_length": 16,
              "original_condition_cases": tested_cases, "generic_control_cases": control_cases,
              "generic_control_hits": control_hits, "known_control": known,
              "large_integer_controls": "three divisors at L=75,b=1, compared with all 75 words",
              "limit_control": "max_nodes=3 correctly returns limited",
              "time_limit_control": "1 ms L=75,b=12 probe correctly returns limited",
              "elapsed_seconds": time.monotonic() - start, "validated_at": now()}
    # Check the real persistence/resume/summary route in disposable storage.
    with tempfile.TemporaryDirectory(prefix="a398769-validation-") as temp:
        args = argparse.Namespace(results=Path(temp), max_length=8, only_length=None,
                                  b=None, case_seconds=1, total_seconds=0)
        run(args, quiet=True)
        before = {p.name: p.read_bytes() for p in Path(temp).glob("length-*.json")}
        run(args, quiet=True)
        assert before == {p.name: p.read_bytes() for p in Path(temp).glob("length-*.json")}
        assert summarize(Path(temp), 8)["largest_fully_verified_length"] == 8
        partial = summarize(Path(temp), 75)
        assert {"length": 75, "b": 12, "status": "missing"} in partial["unfinished_cases"]
        data = load_length(Path(temp), 75)
        data["cases"]["12"] = {"length": 75, "b": 12, "divisor": timed["divisor"],
                               "status": "limited", "search": timed, "build": meta,
                               "witnesses": [], "recorded_at": now()}
        atomic_json(Path(temp) / "length-75.json", data)
        partial = summarize(Path(temp), 75)
        assert {"length": 75, "b": 12, "status": "limited"} in partial["unfinished_cases"]
        assert partial["largest_fully_verified_length"] == 8
    report["resume_control"] = "completed cases unchanged on second run; exact coverage through 8"
    report["incomplete_control"] = "missing and limited cases remain unfinished"
    return report


def load_length(directory, length):
    path = directory / f"length-{length:02d}.json"
    if not path.exists():
        return {"schema": SCHEMA, "source_sha256": source_id(), "length": length, "cases": {}}
    data = json.loads(path.read_text())
    if data.get("schema") != SCHEMA or data.get("source_sha256") != source_id() or data.get("length") != length:
        raise ValueError(f"Incompatible result file: {path}; use a separate result directory")
    for key, record in data["cases"].items():
        b = int(key)
        divisor, reason = parameters(length, b)
        assert record["length"] == length and record["b"] == b and record["divisor"] == str(divisor)
        assert record["status"] in ("excluded", "complete", "limited")
        if record["status"] == "excluded":
            assert reason == record["reason"] and reason is not None
            assert record["witnesses"] == []
        else:
            assert reason is None
            assert record["search"]["status"] == record["status"]
            assert record["search"]["length"] == length and record["search"]["b"] == b
            assert record["search"]["divisor"] == str(divisor)
            assert record["build"]["source_sha256"] == source_id()
            expected_nodes, expected_leaves = work_bound(length, b, divisor)
            assert record["search"]["expected_complete_nodes"] == expected_nodes
            assert record["search"]["expected_complete_leaves"] == expected_leaves
            if record["status"] == "complete":
                assert record["search"]["termination_reason"] == "exhausted"
                assert record["search"]["nodes"] == expected_nodes
                assert record["search"]["leaves"] == expected_leaves
            assert len(record["witnesses"]) == len(record["search"]["witnesses"])
            for item, m in zip(record["witnesses"], record["search"]["witnesses"]):
                assert item == verify_original(3 * int(m), length, b)
    return data


def run(args, quiet=False):
    args.results.mkdir(parents=True, exist_ok=True)
    with (args.results / ".run.lock").open("a") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise RuntimeError("Another writer is using this result directory") from exc
        run_locked(args, quiet)


def run_locked(args, quiet=False):
    meta = ensure_build()
    start = time.monotonic()
    lengths = [args.only_length] if args.only_length else range(1, args.max_length + 1)
    for length in lengths:
        data = load_length(args.results, length)
        counts = [args.b] if args.b is not None else range(length + 1)
        for b in counts:
            divisor, reason = parameters(length, b)
            prior = data["cases"].get(str(b))
            if prior and prior["witnesses"]:
                if not quiet:
                    print(json.dumps({"retained_witnesses": prior["witnesses"]}), flush=True)
                return
            if prior and prior["status"] in ("excluded", "complete"):
                continue
            if args.total_seconds and time.monotonic() - start >= args.total_seconds:
                return
            record = {"length": length, "b": b, "divisor": str(divisor), "recorded_at": now()}
            if reason:
                record.update(status="excluded", reason=reason, witnesses=[])
            else:
                seconds = args.case_seconds
                if args.total_seconds:
                    remaining = max(0.001, args.total_seconds - (time.monotonic() - start))
                    seconds = min(seconds, remaining) if seconds else remaining
                result = engine(length, b, divisor, seconds=seconds)
                record.update(status=result["status"], search=result, build=meta,
                              witnesses=[verify_original(3 * int(m), length, b) for m in result["witnesses"]])
                if prior:
                    record["prior_attempts"] = prior.get("prior_attempts", []) + [
                        {k: v for k, v in prior.items() if k != "prior_attempts"}]
                if not quiet:
                    print(json.dumps({"length": length, "b": b, "status": result["status"],
                                      "elapsed_seconds": result["elapsed_seconds"],
                                      "nodes": result["nodes"], "witnesses": record["witnesses"]}), flush=True)
            data["cases"][str(b)] = record
            atomic_json(args.results / f"length-{length:02d}.json", data)
            if record["witnesses"]:
                return


def summarize(directory, max_length=75):
    rows = []
    unfinished = []
    witnesses = []
    through = 0
    for length in range(1, max_length + 1):
        data = load_length(directory, length)
        counts = {"excluded": 0, "complete": 0, "limited": 0, "missing": 0}
        for b in range(length + 1):
            record = data["cases"].get(str(b))
            # Report mathematical exclusions even if an interrupted run never wrote them.
            divisor, reason = parameters(length, b)
            status = record["status"] if record else ("excluded" if reason else "missing")
            counts[status] += 1
            if status in ("limited", "missing"):
                unfinished.append({"length": length, "b": b, "status": status})
            if record:
                witnesses.extend(record["witnesses"])
        complete = not counts["limited"] and not counts["missing"]
        if complete and through == length - 1:
            through = length
        rows.append({"length": length, **counts, "fully_verified": complete})
    return {"source_sha256": source_id(), "largest_fully_verified_length": through,
            "lengths": rows, "unfinished_cases": unfinished, "witnesses": witnesses,
            "length_75_surviving_cases": [b for b in range(76) if parameters(75, b)[1] is None]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("build")
    validation = sub.add_parser("validate")
    validation.add_argument("--output", type=Path)
    run_parser = sub.add_parser("run")
    run_parser.add_argument("--results", type=Path, default=HERE / "results")
    run_parser.add_argument("--max-length", type=int, default=75)
    run_parser.add_argument("--only-length", type=int)
    run_parser.add_argument("--b", type=int)
    run_parser.add_argument("--case-seconds", type=float, default=0, help="0 means unlimited; limited cases restart on resume")
    run_parser.add_argument("--total-seconds", type=float, default=0)
    summary = sub.add_parser("summarize")
    summary.add_argument("--results", type=Path, default=HERE / "results")
    summary.add_argument("--max-length", type=int, default=75)
    summary.add_argument("--output", type=Path)
    bench = sub.add_parser("benchmark")
    bench.add_argument("--seconds", type=float, default=3)
    bench.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.command == "build":
        result = build()
    elif args.command == "validate":
        result = validate()
    elif args.command == "run":
        if not 1 <= args.max_length <= 75 or (args.only_length is not None and not 1 <= args.only_length <= 75):
            parser.error("length must be in 1..75")
        if args.b is not None and (args.only_length is None or not 0 <= args.b <= args.only_length):
            parser.error("--b requires --only-length and 0 <= b <= length")
        if args.case_seconds < 0 or args.total_seconds < 0:
            parser.error("time budgets must be nonnegative")
        run(args)
        return
    elif args.command == "summarize":
        result = summarize(args.results, args.max_length)
    else:
        if args.seconds <= 0:
            parser.error("benchmark seconds must be positive")
        meta = ensure_build()
        result = {"source_sha256": source_id(), "build": meta, "benchmarked_at": now(), "cases": []}
        for length, b in [(27, 18), (51, 15), (75, 3), (75, 12), (75, 21), (75, 39), (75, 66)]:
            divisor, reason = parameters(length, b)
            if reason:
                result["cases"].append({"length": length, "b": b, "excluded": reason})
            else:
                result["cases"].append(engine(length, b, divisor, seconds=args.seconds))
    if getattr(args, "output", None):
        atomic_json(args.output, result)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
