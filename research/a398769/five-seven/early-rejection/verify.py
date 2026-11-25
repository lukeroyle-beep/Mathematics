#!/usr/bin/env python3
"""Validate source-bound independent receipts; --recompute reruns both audits.

The verifier imports neither implementation. All essential checks survive -O.
It also checks unchanged inherited sources against the actual starting commit.
"""

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
BASELINE = "de64c6da6d616455b69eb9bcf33646ce4e798279"
AUDITED_HEAD = "cd4df1843e8a17655115275e5df956cf985a5819"


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def run(command):
    p = subprocess.run(command, cwd=ROOT, stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE, check=False)
    require(p.returncode == 0, f"failed {command}: {p.stderr.decode()}")
    return p.stdout


def compare(a, b):
    x = a["summary"]
    require([x["categories"][str(k)] for k in range(1, 5)] == b["counts"],
            "partition disagreement")
    for ka, kb in [("first_length", "min_length"), ("last_length", "max_length"),
                   ("lengths", "lengths"), ("actual_representatives", "actual"),
                   ("actual_five_free", "actual_five_free"),
                   ("full_sum_passes", "full_sum_passes"), ("sha256", "sha256")]:
        require(x[ka] == b[kb], f"audit disagreement: {ka}")
    require(len(a["blocks"]) == len(b["blocks"]), "block count disagreement")
    next_length = x["first_length"]
    covered = 0
    for aa, bb in zip(a["blocks"], b["blocks"]):
        for ka, kb in [("first_length", "first"), ("last_length", "last"),
                       ("lengths", "count"), ("sha256", "sha256")]:
            require(aa[ka] == bb[kb], f"mismatch in block starting {next_length}: {ka}")
        require(aa["first_length"] == next_length, "block gap or overlap")
        count = (aa["last_length"] - next_length) // 2 + 1
        require(count == aa["lengths"] and 1 <= count <= 50_000, "block coverage")
        require(count == sum(aa["categories"].values()), "block partition")
        if aa["last_length"] != x["last_length"]:
            require(count == 50_000, "short nonfinal block")
        covered += count
        next_length = aa["last_length"] + 2
    require(covered == x["lengths"] and next_length == x["last_length"] + 2,
            "incomplete block coverage")
    ap, bp = a["prefix_through_100001"], b["prefix_through_100001"]
    require(ap["sha256"] == bp["sha256"], "prefix digest disagreement")
    require(ap["lengths"] == bp["lengths"] == 49_999, "prefix coverage")
    require([ap["categories"][str(k)] for k in range(1, 5)] == bp["counts"],
            "prefix partition disagreement")


def preservation():
    run(["git", "merge-base", "--is-ancestor", BASELINE, "HEAD"])
    run(["git", "merge-base", "--is-ancestor", AUDITED_HEAD, BASELINE])
    paths = run(["git", "ls-tree", "-r", "--name-only", BASELINE,
                 "research/a398769/five-seven", "A398769", "A398769.lean",
                 "lakefile.toml", "lake-manifest.json", "lean-toolchain"]).decode().splitlines()
    hashes = {}
    for path in paths:
        original = run(["git", "show", f"{BASELINE}:{path}"])
        actual = (ROOT / path).read_bytes()
        require(actual == original, f"inherited file changed: {path}")
        hashes[path] = sha(actual)
    # Independently check inherited receipt hashes against their prior manifest.
    inherited = json.loads((HERE.parent / "high-depth/verification.json").read_text())
    for path, expected in inherited["inherited_unchanged_sha256"].items():
        require(hashes[path] == expected, f"prior dependency hash mismatch: {path}")
    for path, expected in inherited["source_sha256"].items():
        actual = sha((HERE.parent / "high-depth" / path).read_bytes())
        require(actual == expected, f"prior source/receipt mismatch: {path}")
    return hashes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--recompute", action="store_true",
                        help="rerun both full audits normally and with -O")
    parser.add_argument("--output", type=Path,
                        help="write this verification receipt to a file")
    args = parser.parse_args()
    receipts, runs = [], []
    for letter in ("a", "b"):
        source = HERE / f"checker_{letter}.py"
        raw = (HERE / f"receipt_{letter}.json").read_bytes()
        receipt = json.loads(raw)
        require(receipt["source_sha256"] == sha(source.read_bytes()),
                f"source hash mismatch: {source.name}")
        if args.recompute:
            for optimized in (False, True):
                command = [sys.executable] + (["-O"] if optimized else []) + [str(source)]
                output = run(command)
                require(output == raw, f"full receipt mismatch: {source.name}, optimized={optimized}")
                runs.append({"source": source.name, "optimized": optimized,
                             "exit_code": 0, "stdout_sha256": sha(output)})
        receipts.append(receipt)
    a, b = receipts[0], receipts[1]["audit"]
    compare(a, b)
    require(a["summary"]["first_length"] == 5 and a["summary"]["last_length"] == 9_999_999,
            "receipt is not the main audit")
    require(b["counts"] == [3_041_861, 392_074, 1_566_063, 0], "reported main row not reproduced")
    require(b["prefix_through_100001"]["counts"] == [21_628, 5_658, 22_713, 0],
            "reported small row not reproduced")
    inherited = preservation()
    invalid = []
    for letter in ("a", "b"):
        for optimized in (False, True):
            for endpoints in [(4, 101), (5, 100), (103, 101), (5, 40_000_001)]:
                command = [sys.executable] + (["-O"] if optimized else []) + [
                    str(HERE / f"checker_{letter}.py"), "--min-length", str(endpoints[0]),
                    "--max-length", str(endpoints[1])]
                p = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                require(p.returncode != 0, f"unsupported input accepted: {command}")
                invalid.append({"source": f"checker_{letter}.py", "optimized": optimized,
                                "endpoints": list(endpoints), "rejected": True})
    result = {"status": "PASS", "baseline_commit": BASELINE, "pr15_audited_head": AUDITED_HEAD,
              "main_interval": [5, 9_999_999], "odd_lengths": b["lengths"],
              "partition": b["counts"], "ordered_sha256": b["sha256"],
              "prefix_sha256": b["prefix_through_100001"]["sha256"],
              "blocks_compared": len(b["blocks"]), "fresh_full_runs": runs,
              "unsupported_input_controls": invalid,
              "inherited_unchanged_sha256": inherited,
              "large_inherited_certificates_rerun": False,
              "new_lean_formalization": False,
              "source_sha256": {p.name: sha(p.read_bytes()) for p in
                                [HERE / "checker_a.py", HERE / "checker_b.py", Path(__file__)]},
              "receipt_sha256": {f"receipt_{c}.json": sha((HERE / f"receipt_{c}.json").read_bytes())
                                 for c in ("a", "b")}}
    output = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(output)
    else:
        print(output, end="")


if __name__ == "__main__":
    main()
