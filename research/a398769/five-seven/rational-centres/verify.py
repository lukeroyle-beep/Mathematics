#!/usr/bin/env python3
"""Check complete, source-bound coverage and pair-stream agreement for all partitions.

This audits retained receipts; it does not rerun the full enumerations. Reproduce
them into empty output directories with the two runners documented in README.md.
"""
import hashlib
import json
from math import gcd
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = "81dce203b1eecc61ec9fda36bc812095e2c89724"
BANDS = ((15, 102, 225, 1000002000001, 4069338437093, 5540084, 2314738),
         (16, 143, 256, 4069338437095, 28485369059657, 7072218, 2945860),
         (17, 227, 288, 28485369059659, 78999999999999, 5624406, 2343851))
CONTROL = (17, 289, 28485369059659, 199397583417605)
COUNTS = ("reduced_numerators", "raw_lines", "compatible_lines", "phase_lines", "roots13",
          "pairs13", "fivefree13", "sum13", "pairs22", "fivefree22", "sum22", "singular_lines")


def require(ok, why):
    if not ok:
        raise RuntimeError(why)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def line_counts(k, b):
    """Count an arithmetic progression in [-k²,k²], without enumerating h."""
    numerators = compatible = phases = singular = 0
    for a in range(1, b):
        if gcd(a, b) != 1:
            continue
        numerators += 1
        g = gcd(3, a)
        m = 2*g
        r = (3*b-a) % m
        count = (k*k-r)//m - (-k*k-1-r)//m
        compatible += count
        phases += count*g
        if a % 7 == 0:
            singular += count
    return dict(reduced_numerators=numerators, raw_lines=numerators*(2*k*k+1),
                compatible_lines=compatible, phase_lines=phases, singular_lines=singular)


def audit(primary_dir, independent_dir):
    targets = [(k, b, lo, hi) for k, first, last, lo, hi, _, _ in BANDS
               for b in range(first, last+1)] + [CONTROL]
    require(len(targets) == len(set(targets)) == 301, "plan uniqueness")
    pnames = {f"K{k}-b{b}" + ("-control" if (k,b,lo,hi)==CONTROL else "") + ".json"
              for k,b,lo,hi in targets}
    inames = {f"K{k}-b{b}.json" for k,b,_,_ in targets}
    for directory, names in ((primary_dir, pnames), (independent_dir, inames)):
        require({f.name for f in directory.iterdir()} == names, "missing, duplicate, or extra partition: " + str(directory))
    all_records, pairs_hash = [], hashlib.sha256()
    for k, b, lo, hi in targets:
        pname = f"K{k}-b{b}" + ("-control" if (k,b,lo,hi)==CONTROL else "") + ".json"
        p = json.loads((primary_dir/pname).read_text())
        q = json.loads((independent_dir/f"K{k}-b{b}.json").read_text())
        for record, source in ((p, "primary.cpp"), (q, "independent.cpp")):
            require(tuple(record[x] for x in ("K", "b", "lo", "hi")) == (k,b,lo,hi), "partition bounds")
            require(record["source_sha256"] == digest(HERE/source), "stale source: " + source)
            require(all(type(record[key]) is int and record[key] >= 0 for key in COUNTS), "nonnegative integer counts")
            for key, value in line_counts(k, b).items():
                require(record[key] == value, "independent exact line count: " + key)
        require(p["baseline"] == q["baseline_commit"] == BASE, "baseline identity")
        require(p["complete"] is True and p["depth"] == 22 and p["at"] == 13, "primary coverage")
        require(p["runner_sha256"] == digest(HERE/"run_primary.py"), "primary runner binding")
        require(q["depth"] == 13 and q["h_limit"] == k*k, "independent coverage")
        for key in COUNTS + ("pairs13_sha256", "pairs22_sha256", "survivors22"):
            require(p[key] == q[key], f"partition disagreement K={k} b={b}: {key}")
        require(p["pairs22"] == len(p["survivors22"]) == 0, "unresolved depth22 survivor")
        require(p["pairs22_sha256"] == hashlib.sha256(b"").hexdigest(), "empty depth22 digest")
        require(p["sum13"] == 0 and p["sum22"] == 0, "sum survivor requires resolution")
        require(0 <= p["fivefree13"] <= p["pairs13"] and p["roots13"] <= p["pairs13"], "count nesting")
        require(lo % 2 == hi % 2 == 1 and lo-2 > 22, "endpoint/depth sufficiency")
        pairs_hash.update(f"{k},{b},{lo},{hi},{p['pairs13_sha256']}\n".encode())
        all_records.append(p)
    bands = []
    for k, first, last, lo, hi, raw, compatible in BANDS:
        records = [r for r in all_records if r["K"] == k and first <= r["b"] <= last]
        require(len(records) == last-first+1, "denominator coverage")
        totals = {field: sum(r[field] for r in records) for field in COUNTS}
        require(totals["raw_lines"] == raw and totals["compatible_lines"] == compatible, "supplied count audit")
        bands.append(dict(K=k, b_first=first, b_last=last, lo=lo, hi=hi,
                          partitions=len(records), **totals))
    require(sum(r["raw_lines"] for r in bands) == 18236708, "all labelled lines")
    require(sum(r["compatible_lines"] for r in bands) == 7604449, "all compatible lines")
    control = all_records[-1]
    for key, value in dict(reduced_numerators=272, raw_lines=157488, compatible_lines=61180,
                           pairs13=562262, fivefree13=449824, sum13=0, pairs22=0).items():
        require(control[key] == value, "original b289 control: " + key)
    return bands, {key: control[key] for key in ("K", "b", "lo", "hi") + COUNTS + ("pairs13_sha256",)}, pairs_hash.hexdigest()


def main():
    bands, control, pair_digest = audit(HERE/"receipts/primary", HERE/"receipts/independent")
    baseline = json.loads((HERE/"baseline.json").read_text())
    require(baseline["starting_main"] == baseline["pr24_final_merge"] == BASE, "baseline commit record")
    require(baseline["pr24_integration"] == "d56df00ef26e24b0e3f1c7e2200b9885adf949e6", "integration identity")
    for relative, expected in baseline["reference_sha256"].items():
        require(digest(HERE.parent/relative) == expected, "baseline source binding: " + relative)
    controls = json.loads((HERE/"controls.json").read_text())
    independent_controls = json.loads((HERE/"independent-controls.json").read_text())
    for record in (controls, independent_controls):
        require(record["status"] == "PASS" and record["positive_sum_occurrences"] > 0
                and record["singular_positive_occurrences"] > 0, "nonvacuous control receipt")
    require(controls["source_sha256"] == {name: digest(HERE/name) for name in ("primary.cpp", "independent.cpp")}, "compiled control binding")
    require(independent_controls["source_sha256"] == digest(HERE/"independent.cpp"), "independent control binding")
    analytic = json.loads((HERE/"analytic-checks.json").read_text())
    require(analytic["status"] == "PASS", "analytic checks")
    for relative, expected in analytic["reference_sha256"].items():
        require(digest(HERE.parent/relative) == expected, "inherited source binding: " + relative)
    files = ["ANALYTIC.md", "SEARCH.md", "README.md", "analytic_checks.py", "analytic-checks.json",
             "primary.cpp", "independent.cpp", "run_primary.py", "independent_runner.py",
             "controls.py", "controls.json", "independent_controls.py", "independent-controls.json", "baseline.json",
             "verify.py", "../../../../README.md"]
    artifacts = {str(p.relative_to(HERE)): digest(p) for p in sorted((HERE/"receipts").glob("*/*.json"))}
    artifacts.update({name: digest(HERE/name) for name in files})
    print(json.dumps({"status": "PASS", "baseline": BASE, "fresh_full_enumerations": ["primary", "independent"],
                      "partitions_per_engine": 300, "control_partitions_per_engine": 1,
                      "bands": bands, "original_b289_control": control,
                      "ordered_partition_pair_digest": pair_digest, "artifact_sha256": artifacts,
                      "unresolved_survivors": [], "whole_length_endpoint": 1000002000000,
                      "all_length_reduced_K_squared_subfamily": "EXCLUDED",
                      "unrestricted_five_seven": "OPEN", "wider_digit_one_conjecture": "OPEN",
                      "new_Lean_formalization": False}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
