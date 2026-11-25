#!/usr/bin/env python3
"""Reproduce the bounded audit and check independent agreement, without asserts."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
BASE = "b6db8703afd3d32211fd75de9ce1e34440dddfe8"
AUDITED = "22ef46d55fa903b54e0b288a1b38ba0a6fa0659a"


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def git(*args):
    return subprocess.run(["git", "-C", str(ROOT), *args], check=True,
                          capture_output=True).stdout


def main():
    git("merge-base", "--is-ancestor", BASE, "HEAD")
    git("merge-base", "--is-ancestor", AUDITED, BASE)
    runs, outputs = [], {}
    for source, receipt in (("checks.py", "checks.json"),
                            ("independent_blocks.py", "independent.json")):
        expected = (HERE / receipt).read_bytes()
        for optimized in (False, True):
            command = [sys.executable] + (["-O"] if optimized else []) + [str(HERE / source)]
            result = subprocess.run(command, capture_output=True, check=True, cwd=ROOT)
            require(result.stdout == expected, f"receipt mismatch: {source}, -O={optimized}")
            runs.append({"source": source, "optimized": optimized,
                         "exit_code": result.returncode, "stdout_sha256": sha(result.stdout)})
        outputs[source] = json.loads(expected)
    a = outputs["checks.py"]["bounded_experiment"]
    b = outputs["independent_blocks.py"]
    comparisons = {
        "ordered_digest": (a["ordered_length_representative_sha256"], b["ordered_sha256"]),
        "odd_lengths": (a["counts"]["odd_lengths"], b["odd_lengths"]),
        "K_counts": (a["lengths_by_K"], b["by_K"]),
        "actual_representatives": (a["counts"]["actual_representatives"], b["actual_representatives"]),
        "five_free_actual": (a["counts"]["actual_5_free_failing_full_sum"] +
                             a["counts"]["actual_5_free_passing_full_sum"],
                             b["actual_with_5_not_dividing_S"]),
        "zero_runs": (a["all_actual_zero_run_histogram"], b["zero_run_histogram"]),
        "full_sum_survivors": (a["full_sum_survivors"], b["full_sum_survivors"]),
    }
    for name, (left, right) in comparisons.items():
        require(left == right, "independent mismatch: " + name)
    require(a["odd_lengths_inclusive"] == [5, b["limit"]], "coverage endpoints")
    require(b["odd_lengths"] == (b["limit"] - 5) // 2 + 1, "coverage count")
    for control in outputs["checks.py"]["saturation_controls"]:
        matches = [x for x in b["order_controls"] if x["L"] == control["L"]]
        require(len(matches) == 1, "order control missing")
        x = matches[0]
        require((x["S"], x["d"], x["e"], x["K"]) ==
                (control["S"], control["order_S"], control["v7_order"], control["K"]),
                "independent order mismatch")
    for label in ("longest_zero_run_control", "longest_5_free_zero_run_control"):
        c = a[label]
        x = next(v for v in b["controls"] if (v["L"], v["i"]) == (c["L"], c["i"]))
        require((x["depth"], x["F_mod_9S"]) == (c["depth"], c["F_mod_9S"]),
                "independent zero-run mismatch")
    # Independent guard: optimizing Python must not disable input validation.
    invalid = []
    for optimized in (False, True):
        cmd = [sys.executable] + (["-O"] if optimized else [])
        cmd += [str(HERE / "independent_blocks.py"), "--limit", "4"]
        result = subprocess.run(cmd, capture_output=True, cwd=ROOT)
        require(result.returncode != 0 and b"bounded audit supports" in result.stderr,
                "invalid-input check disabled")
        invalid.append({"optimized": optimized, "rejected": True})
    prefix = "research/a398769/five-seven/"
    dependencies = [
        "README.md", "settlement/README.md", "settlement/FULL_DIVISOR.md",
        "settlement/EDGE_BOUNDS.md", "settlement/lift_sieve.cpp", "settlement/verify.py",
        "settlement/verify_fixed.py", "settlement/lifting.json", "settlement/independent.json",
        "global/README.md", "global/FIXED_MODULUS.md", "global/TWO_QUOTIENTS.md",
        "global/GROWING_POWER.md", "effective/README.md", "effective/QUALITATIVE.md",
        "effective/ROUTE_A.md", "effective/ROUTE_B.md", "effective/CUTOFF.md",
        "proportional/README.md", "proportional/COVERAGE.md", "proportional/AUDIT.md",
        "depth/README.md", "depth/BOUNDED_DEPTH.md", "depth/PRIME_FILTERS.md",
        "depth/depth_samples.json", "depth/REVIEW.md", "fixed-depth/README.md",
        "fixed-depth/PROOF.md", "fixed-depth/REVIEW.md", "whole-length/README.md",
        "whole-length/PROOF.md", "whole-length/REVIEW.md", "whole-length/checks.json",
        "whole-length/blocks.json", "whole-length/verification.json",
    ]
    inherited = {}
    for relative in dependencies:
        path = prefix + relative
        baseline = git("show", BASE + ":" + path)
        require((ROOT / path).read_bytes() == baseline, "inherited dependency changed: " + path)
        inherited[path] = sha(baseline)
    require(not git("diff", BASE, "--", "A398769", "Mathematics.lean",
                    "lakefile.toml", "lake-manifest.json", "lean-toolchain"), "Lean boundary changed")
    sources = {p.name: sha(p.read_bytes()) for p in sorted(HERE.iterdir())
               if p.is_file() and p.suffix in (".py", ".md", ".json")
               and p.name != "verification.json"}
    result = {"status": "PASS: bounded checks and preservation; subclass remains open",
              "baseline_commit": BASE, "pr14_merge_commit": BASE, "pr14_audited_commit": AUDITED,
              "runs": runs, "independent_comparisons": list(comparisons),
              "ordered_sha256": b["ordered_sha256"], "invalid_input_controls": invalid,
              "source_sha256": sources, "inherited_unchanged_sha256": inherited,
              "large_certificates_rerun": False, "new_lean_formalization": False,
              "new_length_coverage": None, "verdict": 4}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
