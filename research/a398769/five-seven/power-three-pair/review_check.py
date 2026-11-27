#!/usr/bin/env python3
"""Independent exact-commit bindings and original-word review arithmetic."""
import argparse
from hashlib import sha256
import io
import json
from pathlib import Path
import subprocess
import tarfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
BASE = "42e6a151c5279905a3e02b859c6fae737178fd7d"
IMPLEMENTATION = "0a978f53b10122ebeb2059a098005ac02b1bf5c3"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def digest(data):
    return sha256(data).hexdigest()


def word(length, position, modulus):
    # R_L=(10^L-1)/9. Work modulo 9m before exact integer division;
    # this retains all information even when 3 divides m.
    numerator = (pow(10, length, 9*modulus)-1) % (9*modulus)
    require(numerator % 9 == 0, "repunit exact division")
    repunit = numerator // 9
    return (7*repunit-2-2*pow(10, position, modulus)) % modulus


def compute():
    subprocess.run(["git", "merge-base", "--is-ancestor", BASE, IMPLEMENTATION],
                   cwd=ROOT, check=True)
    subprocess.run(["git", "merge-base", "--is-ancestor", IMPLEMENTATION, "HEAD"],
                   cwd=ROOT, check=True)
    require(git("show", "-s", "--format=%P", IMPLEMENTATION).decode().strip() == BASE,
            "implementation starts exactly from requested current main")
    require(git("show", "-s", "--format=%P", BASE).decode().split()[0] ==
            "0a47180b889b392c2323bc1614a473af51f38d78", "PR28 parent")
    changed = git("diff", "--name-only", BASE, IMPLEMENTATION).decode().splitlines()
    require(len(changed) == 20 and "README.md" in changed, "complete implementation path count")
    bindings = {}
    for name in changed:
        committed = git("show", IMPLEMENTATION+":"+name)
        require((ROOT/name).read_bytes() == committed, "changed path differs from reviewed commit: "+name)
        bindings[name] = digest(committed)

    with tarfile.open(fileobj=io.BytesIO(git("archive", BASE))) as archive:
        baseline_bytes = {m.name: archive.extractfile(m).read() for m in archive if m.isfile()}
    recorded = json.loads((HERE/"baseline.json").read_text())
    require({p:digest(b) for p,b in baseline_bytes.items()} == recorded["inherited_sha256"],
            "complete base archive manifest")
    require(len(baseline_bytes) == 1045, "inherited path count")
    for name, data in baseline_bytes.items():
        if name != "README.md":
            require((ROOT/name).read_bytes() == data, "inherited file changed: "+name)
    original = baseline_bytes["README.md"]
    title, rest = original.split(b"\n\n", 1)
    current = (ROOT/"README.md").read_bytes()
    require(current.startswith(title+b"\n\n") and current.endswith(rest), "root README addition scope")

    individual = json.loads((HERE/"individual.json").read_text())
    rows = individual["finite_rows_including_crossing_successor"] + [individual["new_a1567"]]
    require([r["a"] for r in rows] == list(range(31, 104, 6))+[1567], "finite and next-member coverage")
    rows += [individual["controls"]["a25"]]
    checked = []
    for row in rows:
        a, length, position, total = row["a"], row["L"], row["s"], row["S"]
        require(total == 3**a and 7*length == total+4, "sum and length")
        require(3 <= position < 2*3**(a-2) and position % 6 == 3, "joint class domain")
        f = (7*pow(10, length, 9*total)-18*pow(10, position, 9*total)-25) % (9*total)
        require(f == 0, "full sum readback")
        if not row["actual"]:
            require(position >= length and row["verdict"] == "class_miss", "class miss readback")
            checked.append({"a":a, "actual":False})
            continue
        require(position < length and word(length, position, total) == 0 and
                word(length, position, 25*total) == 0, "original non-seven factors")
        depth = row["first_fail_depth"]
        residues = [word(length, position, 7**j) for j in range(1, depth+1)]
        require(residues == row["seven_residues"] == [0]*(depth-1)+[row["first_fail_n_residue"]],
                "independent original-word first failure")
        require(0 < residues[-1] < 7**depth and depth <= length-2 and row["t"] == depth-1,
                "inclusive threshold and finite valuation")
        checked.append({"a":a, "actual":True, "valuation":depth-1, "original_word_residues":residues})
    new = next(r for r in checked if r["a"] == 1567)
    require(new["valuation"] == 1 and new["original_word_residues"] == [0,7], "new individual verdict")
    require(word(313, 51, 2187) == 1944, "lost-nine original word")
    require((7*pow(10,313,9*2187)-18*pow(10,51,9*2187)-25) % (9*2187) == 17496,
            "lost-nine full F residue")
    verification = json.loads((HERE/"verification.json").read_text())
    require(verification["status"] == "PASS" and len(verification["corruption_controls_rejected"]) == 9,
            "aggregate controls")
    require(verification["whole_length_endpoint_inclusive"] == 1000002000000 and
            verification["individual_family"] == verification["unrestricted_five_seven"] ==
            verification["wider_digit_one"] == "OPEN", "separate scope")

    return {
        "schema":"a398769-adjacent-pair-final-review-v1",
        "reviewer_context":"/root/eliminant_review", "builder_context":"/root",
        "reviewed_implementation_commit":IMPLEMENTATION, "base_main":BASE,
        "implementation_changed_paths":len(changed), "implementation_sha256":bindings,
        "inherited_paths_bound":len(baseline_bytes), "unchanged_inherited_paths":len(baseline_bytes)-1,
        "review_only_sha256":{name:digest((HERE/name).read_bytes()) for name in ("REVIEW.md","review_check.py")},
        "independent_repunit_rows":checked,
        "aggregate_corruptions_rejected":verification["corruption_controls_rejected"],
        "pair_theorem":"PROVED for every u>=0", "individual_family":"OPEN",
        "whole_length_endpoint_inclusive":1000002000000,
        "unrestricted_five_seven":"OPEN", "wider_digit_one":"OPEN",
        "Lean_verification_performed":False, "result":"PASS",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", type=Path)
    args = parser.parse_args()
    encoded = json.dumps(compute(), sort_keys=True, indent=2)+"\n"
    if args.check:
        require(args.check.read_text() == encoded, "source-bound final review receipt differs")
        print("PASS: exact implementation commit, complete bindings, independent original words")
    else:
        print(encoded, end="")


if __name__ == "__main__":
    main()
