#!/usr/bin/env python3
"""Independently audit the retained complete {3,9} search through 75 digits.

Usage: python3 audit_results.py [SEARCH_DIRECTORY] [--output RECEIPT.json]
Default SEARCH_DIRECTORY is the directory containing this script. This does not
import search.py or rerun the expensive search. It independently verifies the
arithmetic exclusions, exact traversal counts, complete checkpoint coverage and
artifact consistency. It is a computational-record audit, not a Lean proof.
"""
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sys

MAX_LENGTH = 75
SURVIVING_75 = [3, 12, 21, 39, 48, 57, 66]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def read_json(path):
    return json.loads(path.read_text(), object_pairs_hook=unique_object)


def natural(value, label):
    require(type(value) is int and value >= 0, f"Invalid count: {label}")
    return value


def source_hash(directory):
    digest = hashlib.sha256()
    for name in ("search.cpp", "search.py"):
        digest.update(name.encode() + b"\0" + (directory / name).read_bytes())
    return digest.hexdigest()


def exclusion(length, b, divisor):
    # Independent mathematical necessities, in the recorded priority order.
    digit_sum_of_m = length + 2 * b
    if length % 2 == 0:
        return "even_length"
    modulus = 9 if length + b >= 2 else 3
    if digit_sum_of_m % modulus:
        return "digit_sum_mod_9_or_3"
    if digit_sum_of_m % 5 == 0:
        return "factor_5"
    greatest_m = int("3" * b + "1" * (length - b))
    if divisor > greatest_m:
        return "divisor_above_maximum"
    return None


def independent_tree_size(length, b, divisor):
    # Count reachable states level by level, with path multiplicities. This
    # intentionally differs from search.py's recursive memoized calculation.
    states = {(length, b): 1}
    nodes = leaves = 0
    while states:
        following = Counter()
        for (remaining, needed), multiplicity in states.items():
            nodes += multiplicity
            # Put the required threes at the right or left of an all-one suffix.
            low_increment = 2 * int("1" * needed or "0")
            high_increment = low_increment * 10 ** (remaining - needed)
            if high_increment - low_increment < 2 * divisor:
                leaves += multiplicity
            else:
                if needed < remaining:
                    following[remaining - 1, needed] += multiplicity
                if needed:
                    following[remaining - 1, needed - 1] += multiplicity
        states = following
    return nodes, leaves


def audit(directory):
    expected_source = source_hash(directory)
    validation = read_json(directory / "validation.json")
    require(validation["status"] == "passed", "Validation did not pass")
    require(validation["source_sha256"] == expected_source, "Validation source mismatch")
    require(validation["build"]["source_sha256"] == expected_source, "Validation build source mismatch")
    expected_binary = validation["build"]["binary_sha256"]
    require(re.fullmatch(r"[0-9a-f]{64}", expected_binary) is not None, "Invalid binary hash")
    require(validation["original_condition_max_length"] >= 16, "Insufficient direct validation range")
    require(validation["original_condition_words"] == 131070, "Unexpected direct validation word count")
    require(validation["generic_control_hits"] > 0, "Missing positive-control evidence")
    require(validation["known_control"] == ["111133131", "111331113", "113131311",
                                            "133113111", "311113311"], "Known control mismatch")

    results = directory / "results"
    expected_files = {f"length-{length:02d}.json" for length in range(1, MAX_LENGTH + 1)}
    require({path.name for path in results.glob("length-*.json")} == expected_files,
            "Missing or extra length checkpoint files")
    totals = Counter()
    lengths = []
    terminal_cases_75 = []
    total_seconds = 0.0
    for length in range(1, MAX_LENGTH + 1):
        data = read_json(results / f"length-{length:02d}.json")
        require(data["schema"] == 1 and data["length"] == length, f"Bad checkpoint identity: {length}")
        require(data["source_sha256"] == expected_source, f"Checkpoint source mismatch: {length}")
        require(set(data["cases"]) == {str(b) for b in range(length + 1)},
                f"Missing or extra digit-count cases: {length}")
        completed = []
        excluded = Counter()
        for b in range(length + 1):
            record = data["cases"][str(b)]
            label = f"L={length}, b={b}"
            divisor = 3 ** (length + b) * (length + 2 * b)
            require(record["length"] == length and record["b"] == b and
                    record["divisor"] == str(divisor), f"Case identity mismatch: {label}")
            require(record["witnesses"] == [], f"Witness requires separate direct verification: {label}")
            reason = exclusion(length, b, divisor)
            totals["cases"] += 1
            if reason is not None:
                require(record["status"] == "excluded" and record["reason"] == reason,
                        f"Exclusion mismatch: {label}")
                excluded[reason] += 1
                totals[reason] += 1
                totals["excluded"] += 1
                continue
            require(record["status"] == "complete", f"Unfinished case: {label}")
            search = record["search"]
            require(search["status"] == "complete" and search["termination_reason"] == "exhausted",
                    f"Traversal not exhausted: {label}")
            require(search["engine"] == "stage4-prefix-v1", f"Unexpected engine: {label}")
            require(search["length"] == length and search["b"] == b and
                    search["divisor"] == str(divisor), f"Engine identity mismatch: {label}")
            require(search["witnesses"] == [], f"Engine witness requires direct verification: {label}")
            require(record["build"]["source_sha256"] == expected_source and
                    record["build"]["binary_sha256"] == expected_binary, f"Build hash mismatch: {label}")
            nodes, leaves = independent_tree_size(length, b, divisor)
            for key, expected in (("nodes", nodes), ("leaves", leaves),
                                  ("expected_complete_nodes", nodes), ("expected_complete_leaves", leaves)):
                require(natural(search[key], label + ":" + key) == expected,
                        f"Traversal count mismatch: {label}, {key}")
            candidates = natural(search["candidates_tested"], label + ":candidates_tested")
            require(candidates <= leaves, f"Too many candidates: {label}")
            elapsed = search["elapsed_seconds"]
            require(type(elapsed) in (int, float) and 0 <= elapsed < float("inf"),
                    f"Invalid elapsed time: {label}")
            total_seconds += elapsed
            for key, value in (("nodes", nodes), ("leaves", leaves), ("candidates_tested", candidates)):
                totals[key] += value
            totals["complete"] += 1
            completed.append(b)
            if length == 75:
                terminal_cases_75.append({"b": b, "status": "complete", "witnesses": [],
                                          "nodes": nodes, "leaves": leaves,
                                          "candidates_tested": candidates, "elapsed_seconds": elapsed})
        lengths.append({"length": length, "fully_verified": True,
                        "complete": len(completed), "excluded": sum(excluded.values()),
                        "completed_digit_counts": completed, "exclusion_reasons": dict(excluded)})
    require(totals["cases"] == 2925, "Incorrect total case count")
    require(lengths[-1]["completed_digit_counts"] == SURVIVING_75, "Length-75 survivor mismatch")

    coverage = read_json(directory / "coverage.json")
    require(coverage["source_sha256"] == expected_source, "Coverage source mismatch")
    require(coverage["largest_fully_verified_length"] == MAX_LENGTH and
            coverage["unfinished_cases"] == [] and coverage["witnesses"] == [], "Incomplete coverage report")
    require(coverage["length_75_surviving_cases"] == SURVIVING_75, "Coverage survivor mismatch")
    require([row["length"] for row in coverage["lengths"]] == list(range(1, MAX_LENGTH + 1)),
            "Coverage length ordering or membership mismatch")
    for expected, reported in zip(lengths, coverage["lengths"]):
        require(reported["fully_verified"] is True and reported["missing"] == 0 and reported["limited"] == 0,
                f"Coverage incomplete at {expected['length']}")
        require(all(reported[key] == expected[key] for key in ("length", "complete", "excluded")),
                f"Coverage count mismatch at {expected['length']}")
    return {"status": "passed", "audited_at": datetime.now(timezone.utc).isoformat(),
            "audit_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "source_sha256": expected_source, "recorded_binary_sha256": expected_binary,
            "binary_check": "All completed records match validation build hash; no local executable required",
            "method": "Direct arithmetic exclusions and independent level-by-level traversal counts",
            "claim": "Finite computational coverage of all {3,9} integers with 1 through 75 digits; no witnesses",
            "limitation": "Audits retained execution records and source binding; does not rerun searches or supply a Lean proof",
            "largest_fully_verified_length": MAX_LENGTH, "unfinished_cases": [], "witnesses": [],
            "totals": dict(totals), "summed_engine_seconds": total_seconds,
            "length_75_cases": terminal_cases_75, "lengths": lengths}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", nargs="?", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        report = audit(args.directory)
    except (OSError, KeyError, TypeError, ValueError) as error:
        print(f"Audit failed: {error}", file=sys.stderr)
        return 1
    text = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text)
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
