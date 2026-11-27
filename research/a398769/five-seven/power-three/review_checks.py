#!/usr/bin/env python3
"""Independent review checks and complete reviewed-source receipt.

This script imports no implementation arithmetic. It re-evaluates the
original decimal repunit expression at every reported individual class,
checks all actual exclusions, and compares the two transition methods.
Use --check to bind the computed report to the archived reviewed sources.
"""
import argparse
from collections import Counter
from fractions import Fraction
import hashlib
import io
import json
from math import factorial
from pathlib import Path
import subprocess
import tarfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
BASE = "0a47180b889b392c2323bc1614a473af51f38d78"
IMPLEMENTATION = "8d56670602fe57280b10ab7a5221941438f28f2c"


def need(condition, message):
    if not condition:
        raise RuntimeError(message)


def read(name):
    return json.loads((HERE / name).read_text())


def sparse_n(length, position, modulus):
    """7 times a decimal repunit minus the two changed digit contributions.

    Division by nine is performed on an integer residue modulo 9*modulus.
    Only when position<length is this expression called an original word.
    """
    power = pow(10, length, 9 * modulus)
    need((power - 1) % 9 == 0, "repunit exact division")
    repunit = (power - 1) // 9
    return (7 * repunit - 2 * pow(10, position, modulus) - 2) % modulus


def individual_review():
    primary = read("individuals.json")
    independent = read("individuals-independent.json")
    need(primary["cases"] == independent["cases"], "individual implementations disagree")
    rows = primary["cases"]
    need([r["a"] for r in rows] == list(range(31, 1562, 6)), "individual scope")
    old = json.loads((HERE.parent / "sum-position-escape/independent.json").read_text())
    need(rows[:128] == old["cases"], "inherited prefix changed")
    histogram = Counter()
    misses = 0
    reviewed = []
    for row in rows:
        a, s = row["a"], row["s"]
        S = 3 ** a
        L = (S + 4) // 7
        d = 3 ** (a - 2)
        need((row["L"], row["S"], row["d"], row["D"]) == (L, S, d, 2*d),
             "individual parameter corruption")
        need(7*L == S+4 and 3 <= s < 2*d and s % 6 == 3 and 2*d > L,
             "joint class or endpoint corruption")
        need(sparse_n(L, s, S) == 0, "original sum equation failed")
        need((s < L) == (row["i"] is not None), "actual versus class-miss classification")
        if row["i"] is None:
            misses += 1
            need(all(row[k] is None for k in ("t", "first_fail_depth", "first_fail_n_residue")),
                 "miss carries a fabricated valuation")
            continue
        need(row["i"] == s, "same position lost")
        need(sparse_n(L, s, 25*S) == 0, "non-seven divisor failed")
        t = row["t"]
        depth = t + 1
        need(row["first_fail_depth"] == depth and 1 <= depth <= L-2,
             "failure is too late to exclude")
        need(sparse_n(L, s, 7**t) == 0, "preceding seven power failed")
        value = sparse_n(L, s, 7**depth)
        need(value != 0 and value == row["first_fail_n_residue"],
             "original word first-failure residue")
        histogram[str(t)] += 1
        reviewed.append({"a": a, "t": t, "failure_modulus": 7**depth, "n_residue": value})
    for data in (primary, independent):
        need(data["class_misses"] == misses and data["actual_candidates"] == len(reviewed),
             "individual totals")
        need(data["valuation_histogram"] == dict(sorted(histogram.items())), "histogram")

    # Independent original-word controls at both special inputs named by Luke.
    control = primary["control_a25"]
    need(control == independent["control_a25"], "a25 control disagreement")
    need(sparse_n(control["L"], control["i"], 3**25) == 0,
         "a25 positive sum control failed")
    need(sparse_n(control["L"], control["i"], 49) == 0 and
         sparse_n(control["L"], control["i"], 343) == 294,
         "a25 exact seven valuation")
    need(sparse_n(313, 51, 2187) == 1944, "lost-nine negative missed")

    # Read back theta, C and kappa at their separately declared precisions.
    theta, C, kappa = [primary[k] for k in ("theta_residue", "C_residue", "kappa_residue")]
    pe = primary["theta_modulus_exponent"]
    ce = primary["C_modulus_exponent"]
    ke = primary["kappa_modulus_exponent"]
    need((pe, ce, ke) == (1564, 1562, 1560), "3-adic precision declaration")
    need(theta % 9 == 1 and pow(theta, 7, 3**pe) == 10000 % 3**pe, "theta readback")
    need((7*theta-25-18*C) % 3**pe == 0, "C precision readback")
    need(pow(10, kappa, 3**ce) == C and kappa % 9 == 6, "kappa readback")
    need(all((r["s"]-kappa) % r["d"] == 0 for r in rows), "every class comes from kappa")
    next_row = rows[128]
    return {"exponents": {"first": 31, "step": 6, "count": 256, "last": 1561,
                           "next_unchecked": 1567},
            "class_misses": misses, "actual_candidates": len(reviewed),
            "valuation_histogram": dict(sorted(histogram.items())),
            "original_word_failures": reviewed,
            "a799": {key: next_row[key] for key in
                     ("a", "t", "first_fail_depth", "first_fail_n_residue")},
            "old_prefix_rows_checked": 128,
            "a25_control": {"sum_residue": 0, "n_mod_49": 0, "n_mod_343": 294},
            "lost_nine_control": {"L": 313, "i": 51, "n_mod_S": 1944}}


def transition_review():
    direct, lifted = read("transitions.json"), read("transitions-independent.json")
    rows = []
    for data in direct["levels"]:
        m = data["m"]
        other = next(r for r in lifted["levels"] if r["m"] == m)
        need(data["period"] == other["period"] == 7**(m-2), "period declaration")
        need(data["starts"] == other["starts"], "transition methods disagree")
        need(data["two_transition_start_count"] == len(data["starts"]) == other["start_count"],
             "transition count corruption")
        need(data["visited_starts"] == data["period"], "full direct period not visited")
        rows.append({"m": m, "period": data["period"], "count": len(data["starts"])})
    need([r["m"] for r in rows] == list(range(5, 10)), "transition depth scope")
    need(rows[-1]["count"] == 0, "depth nine conclusion false")
    need(lifted["positive_control"] in lifted["levels"][-2]["starts"],
         "positive transition control absent")
    return {"complete_periods": rows, "all_start_and_increment_lists_agree": True,
            "direct_visited_starts": sum(r["period"] for r in rows),
            "depth_eight_positive": lifted["positive_control"]}


def source_bindings():
    required = ["README.md", "INDIVIDUAL.md", "THREE_LENGTH.md", "verify.py",
                "baseline.json", "verification.json", "individuals.py", "individuals.json",
                "individuals_independent.py", "individuals-independent.json",
                "transitions.py", "transitions.json", "transitions_independent.py",
                "transitions-independent.json", "review_checks.py"]
    paths = [HERE / name for name in required] + [ROOT / "README.md"]
    paths += [HERE.parent / name for name in
              ("sum-position-escape/README.md", "sum-position-escape/MATH_REVIEW.md",
               "sum-position-escape/independent.py", "sum-position-escape/independent.json",
               "fixed-depth/PROOF.md", "effective/QUALITATIVE.md",
               "settlement/EDGE_BOUNDS.md", "effective/ROUTE_A.md",
               "uniform-bound/SOURCES.md")]
    result = {}
    for path in paths:
        need(path.is_file(), "missing reviewed source: " + str(path))
        relative = str(path.relative_to(ROOT))
        result[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
        if path.name != "review_checks.py":
            committed = subprocess.check_output(["git", "show", IMPLEMENTATION + ":" + relative], cwd=ROOT)
            need(hashlib.sha256(committed).hexdigest() == result[relative],
                 "reviewed implementation changed: " + relative)
    for program, receipt in [("individuals.py", "individuals.json"),
                             ("individuals_independent.py", "individuals-independent.json"),
                             ("transitions.py", "transitions.json"),
                             ("transitions_independent.py", "transitions-independent.json")]:
        need(read(receipt)["source_sha256"] == hashlib.sha256((HERE/program).read_bytes()).hexdigest(),
             "stale implementation receipt: " + receipt)
    need(read("individuals-independent.json")["inherited_source_sha256"] ==
         hashlib.sha256((HERE.parent / "sum-position-escape/independent.py").read_bytes()).hexdigest(),
         "stale inherited adapter source")
    return dict(sorted(result.items()))


def mathematical_constants():
    norm = Fraction(7**7 * 10**4 - 25**7, 18**7)
    need(norm == Fraction(236879375, 68024448), "algebraic norm")
    valuations = {}
    for p in (2, 5):
        numerator, denominator = norm.numerator, norm.denominator
        value = 0
        while numerator % p == 0:
            numerator //= p
            value += 1
        while denominator % p == 0:
            denominator //= p
            value -= 1
        valuations[str(p)] = value
    need(valuations == {"2": -7, "5": 4}, "norm valuations")
    need(36*7**4*12 == 1037232, "explicit logarithm constant")
    need(sum(Fraction(4**k, factorial(k)) for k in range(10)) > 53,
         "rational proof of log53<4")
    return {"norm_C": str(norm), "norm_valuations": valuations,
            "BL_p": 3, "BL_e": 1, "BL_f": 1, "BL_D": 7,
            "BL_log_A1": 3, "BL_log_A2": 4, "BL_simplified_constant": 1037232,
            "primary_source_reopened": "https://irma.math.unistra.fr/~bugeaud/travaux/logpadicdef.pdf",
            "primary_source_scope": "definitions pp.2-4 and Corollary 2 printed p.5",
            "fresh_raw_source_hash_claimed": False}


def baseline_review():
    """Bind the baseline independently to bytes from the actual Git base."""
    baseline = read("baseline.json")
    need(baseline["starting_main"] == baseline["requested_pr27_merge"] == BASE,
         "baseline identity")
    archive_bytes = subprocess.check_output(["git", "archive", BASE], cwd=ROOT)
    archived = {}
    with tarfile.open(fileobj=io.BytesIO(archive_bytes)) as archive:
        for entry in archive:
            if entry.isfile():
                archived[entry.name] = hashlib.sha256(archive.extractfile(entry).read()).hexdigest()
    need(archived == baseline["inherited_sha256"], "baseline differs from exact Git archive")
    need(len(archived) == 1028, "inherited file count")
    changed = []
    for path, expected in archived.items():
        if hashlib.sha256((ROOT/path).read_bytes()).hexdigest() != expected:
            changed.append(path)
    need(changed == ["README.md"], "unexpected inherited changes")
    return {"exact_git_archive_files": len(archived), "modified_inherited_files": changed,
            "unchanged_inherited_files": len(archived)-len(changed)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", type=Path, help="compare exact result with archived receipt")
    args = parser.parse_args()
    subprocess.run(["git", "merge-base", "--is-ancestor", BASE, "HEAD"],
                   cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
    subprocess.run(["git", "merge-base", "--is-ancestor", IMPLEMENTATION, "HEAD"],
                   cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
    result = {"schema": 1, "base_main": BASE, "reviewed_implementation": IMPLEMENTATION,
              "reviewer": "/root/independent_transitions",
              "source_sha256": source_bindings(), "individual_review": individual_review(),
              "transition_review": transition_review(),
              "mathematical_constants": mathematical_constants(),
              "baseline_review": baseline_review(), "verdict": "PASS"}
    output = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.check:
        need(args.check.read_text() == output, "review receipt mismatch")
    print(output, end="")


if __name__ == "__main__":
    main()
