#!/usr/bin/env python3
"""Compile and resume primary enumeration, with atomic per-denominator receipts."""
import argparse
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
BASELINE = "81dce203b1eecc61ec9fda36bc812095e2c89724"
BANDS = [(15, 102, 225, 1000002000001, 4069338437093),
         (16, 143, 256, 4069338437095, 28485369059657),
         (17, 227, 288, 28485369059659, 78999999999999)]
CONTROL = (17, 289, 28485369059659, 199397583417605)


def digest(path):
    with open(path, "rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def partitions():
    return [(k, b, lo, hi) for k, first, last, lo, hi in BANDS
            for b in range(first, last + 1)] + [CONTROL]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--jobs", type=int, default=2)
    parser.add_argument("--only", choices=["control", "bands", "all"], default="all")
    parser.add_argument("--output", type=Path, default=HERE / "receipts" / "primary")
    args = parser.parse_args()
    if not 1 <= args.jobs <= 8:
        parser.error("jobs must be in 1..8")
    args.output.mkdir(parents=True, exist_ok=True)
    selected = partitions()
    if args.only == "control": selected = [CONTROL]
    if args.only == "bands": selected = selected[:-1]
    binding = {"schema": 1, "engine": "primary", "baseline": BASELINE,
               "source_sha256": digest(HERE / "primary.cpp"),
               "runner_sha256": digest(__file__),
               "compile_flags": ["-O3", "-std=c++17", "-Wall", "-Wextra"]}
    with tempfile.TemporaryDirectory(prefix="a398769-primary-") as tmp:
        scratch = Path(tmp)
        binary = scratch / "enumerator"
        subprocess.run(["clang++", *binding["compile_flags"], str(HERE / "primary.cpp"),
                        "-o", str(binary)], check=True)

        def run(part):
            k, b, lo, hi = part
            name = f"K{k}-b{b}" + ("-control" if part == CONTROL else "")
            output = args.output / (name + ".json")
            identity = dict(binding, K=k, b=b, lo=lo, hi=hi, depth=22, at=13)
            if output.exists():
                record = json.loads(output.read_text())
                if any(record.get(key) != value for key, value in identity.items()):
                    raise RuntimeError(f"stale receipt: {output}; use a new --output directory")
                if record.get("complete") is not True:
                    raise RuntimeError(f"incomplete receipt: {output}")
                return name, "retained", record["pairs13"]
            with tempfile.TemporaryDirectory(prefix=name + "-", dir=scratch) as work:
                work = Path(work)
                command = [str(binary), "--K", str(k), "--b", str(b), "--lo", str(lo),
                           "--hi", str(hi), "--pairs", str(work / "pairs.csv"),
                           "--pairs22", str(work / "pairs22.csv"), "--json", str(work / "counts.json")]
                subprocess.run(command, check=True)
                record = json.loads((work / "counts.json").read_text())
                if any(record.get(key) != identity[key] for key in ("K", "b", "lo", "hi", "depth", "at")):
                    raise RuntimeError("output identity mismatch")
                record.update(binding, complete=True,
                              pairs13_sha256=digest(work / "pairs.csv"),
                              pairs22_sha256=digest(work / "pairs22.csv"))
                # Deep survivors are retained in full even when the stream is discarded.
                record["survivors22"] = [list(map(int, line.split(",")))
                                         for line in (work / "pairs22.csv").read_text().splitlines()]
                staged = output.with_suffix(".json.tmp")
                staged.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
                os.replace(staged, output)
                return name, "completed", record["pairs13"]

        with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:
            futures = [pool.submit(run, p) for p in selected]
            for f in concurrent.futures.as_completed(futures):
                print(*f.result(), flush=True)


if __name__ == "__main__":
    main()
