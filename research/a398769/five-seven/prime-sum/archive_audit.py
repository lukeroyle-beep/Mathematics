#!/usr/bin/env python3
"""Audit the recovered archive and verify its candidates from decimal runs.

No imports from either enumerator or the archived verification programs.
Use --rerun-enumerations for two complete fresh searches (several minutes).
External fresh outputs can instead be supplied with --lattice-output and
--floor-output; these are verified, not claimed to have been generated here.
"""
import argparse
from collections import Counter
import hashlib
import io
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

HERE = Path(__file__).resolve().parent
ZIP_HASH = "b657f158d6362c77c570b87c3c193fe54c6f3c385889379edf5bf79b71f05c0a"
PAIR_HASH = "919c091c978ee1e6011f9239fadbba675985714f286d8dcffa1a29ed043cf8e4"
PREFIX = "A398769-research/"
UPPER = 10**12


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def join(left, right, modulus):
    """Concatenate blocks (decimal value mod m, 10**length mod m)."""
    return ((left[0] * right[1] + right[0]) % modulus,
            left[1] * right[1] % modulus)


def repeat_digit(digit, count, modulus):
    require(count >= 0, "negative run")
    answer, block = (0, 1), (digit % modulus, 10 % modulus)
    while count:
        if count & 1:
            answer = join(answer, block, modulus)
        block = join(block, block, modulus)
        count //= 2
    return answer


def decimal_runs(length, position, modulus):
    require(3 <= position < length, "invalid second-five position")
    result = (0, 1)
    for digit, count in ((7, length-position-1), (5, 1),
                         (7, position-1), (5, 1)):
        result = join(result, repeat_digit(digit, count, modulus), modulus)
    return result[0]


def parse_pairs(data, separator):
    pairs = [tuple(map(int, line.split(separator)))
             for line in data.decode("ascii").splitlines()]
    require(all(len(pair) == 2 for pair in pairs), "pair arity")
    require(len(pairs) == len(set(pairs)), "duplicate candidate")
    return sorted(pairs)


def verify_archive(path):
    raw = path.read_bytes()
    require(len(raw) == 920596 and sha(raw) == ZIP_HASH, "archive identity")
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        require(len(z.namelist()) == 28 and z.testzip() is None, "archive integrity")
        files = {name[len(PREFIX):]: z.read(name) for name in z.namelist()}
    manifest = files["SHA256SUMS.txt"].decode().splitlines()
    require(len(manifest) == 27, "manifest count")
    listed = set()
    for line in manifest:
        digest, name = line.split("  ", 1)
        require(name in files and sha(files[name]) == digest, "member identity: " + name)
        listed.add(name)
    require(listed | {"SHA256SUMS.txt"} == set(files), "unlisted archive member")
    candidate_bytes = files["valuation/candidates.csv"]
    require(sha(candidate_bytes) == PAIR_HASH, "candidate identity")
    pairs = parse_pairs(candidate_bytes, ",")
    require(len(pairs) == 74601, "candidate count")
    require(candidate_bytes == "".join(f"{l},{i}\n" for l, i in pairs).encode(),
            "candidate canonical ordering")
    return files, pairs


def check_decimal(pairs):
    modulus = 7**28
    histogram, maxima = Counter(), []
    for length, position in pairs:
        require(5 <= length <= UPPER and length % 2 == 1,
                "candidate length outside domain")
        require(3 <= position < length and position % 6 == 3,
                "candidate position outside domain")
        residue = decimal_runs(length, position, modulus)
        require(residue != 0, "depth 28 survivor needs further verification")
        depth, quotient = 0, residue
        while quotient % 7 == 0:
            quotient //= 7
            depth += 1
        require(depth >= 22, "false depth-22 pair")
        histogram[depth] += 1
        if depth == 27:
            digit_sum = 7*(length-2) + 2*5
            maxima.append({"L": length, "i": position,
                           "F_over_7_27_mod_7": 9*quotient % 7,
                           "F_mod_9S": 9*decimal_runs(length, position, digit_sum)})
    require(dict(histogram) == {22: 63974, 23: 9161, 24: 1272,
                               25: 162, 26: 29, 27: 3}, "depth histogram")
    small = 0
    for length in range(5, 30, 2):
        for position in range(3, length):
            word = "7"*(length-position-1) + "5" + "7"*(position-1) + "5"
            n = int(word)
            require(len(word) == length and word.count("5") == 2, "word construction")
            require(sum(map(int, word)) == 7*length-4, "literal digit sum")
            require(n % 7**(length-2) != 0, "small word reaches witness depth")
            for mod in (49, 225*(7*length-4)*7**(length-2)):
                require(decimal_runs(length, position, mod) == n % mod,
                        "concatenation differs from literal decimal")
            small += 1
    require(small == 182, "small-domain endpoint")
    # This is a positive full digit-sum control, not a full witness.
    require(decimal_runs(61, 57, 423) == 0, "nonzero sum-compatible control")
    require(9*decimal_runs(61, 57, 49) % 49 == 35, "control exact low-depth failure")
    return {"candidate_count": len(pairs), "exact_valuation_histogram": dict(sorted(histogram.items())),
            "maximum_pairs": maxima, "literal_small_words": small,
            "positive_sum_only_control": [61, 57], "full_witnesses": 0}


def compare_outputs(pairs, lattice, floor):
    result = {}
    if lattice is not None:
        data = lattice.read_bytes()
        require(parse_pairs(data, None) == pairs, "lattice candidate mismatch")
        result["lattice"] = {"sha256": sha(data), "pairwise_matches": len(pairs)}
    if floor is not None:
        data = floor.read_bytes()
        lines = data.decode("ascii").splitlines()
        expect = ("B 1000000000000 seeds 121060821 rectangular 1044321 "
                  "domainDepth 21 domainCount 522020 pass22 74601 sig 18130229677626043502")
        require(lines[-1] == expect, "floor count/endpoints differ")
        require(all(line.startswith("depth22 ") for line in lines[:-1]), "unexpected floor row")
        converted = "\n".join(line[len("depth22 "):] for line in lines[:-1]).encode()
        require(parse_pairs(converted, None) == pairs, "floor candidate mismatch")
        result["floor"] = {"sha256": sha(data), "pairwise_matches": len(pairs), "summary": expect}
    return result


def rerun(files, pairs):
    with tempfile.TemporaryDirectory(prefix="a398769-archive-audit-") as temporary:
        root = Path(temporary)
        for name, data in files.items():
            destination = root / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(data)
        lat, floor = root / "lattice-run", root / "floor-run"
        subprocess.run(["g++", "-O3", "-std=c++17", str(root/"valuation/lattice/lattice.cpp"),
                        "-o", str(lat)], check=True)
        subprocess.run(["g++", "-O3", "-std=c++17", "-DDEPTH=11",
                        str(root/"valuation/floor-sum/scan.cpp"), "-o", str(floor)], check=True)
        lp, fp = root / "lattice.txt", root / "floor.txt"
        log = subprocess.check_output([str(lat), "10", str(UPPER), str(lp)], text=True).strip()
        expected = ("limit 1000000000000 base_depth 10 groups 17294403 depth_19 25586997 "
                    "depth_20 3654595 depth_21 522020 depth_22 74601")
        require(log == expected, "lattice summary")
        with fp.open("wb") as output:
            subprocess.run([str(floor), str(UPPER)], stdout=output, check=True)
        return {"mode": "freshly_executed", "lattice_summary": log,
                "outputs": compare_outputs(pairs, lp, fp)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path, default=HERE/"evidence/trillion-evidence.zip")
    parser.add_argument("--lattice-output", type=Path)
    parser.add_argument("--floor-output", type=Path)
    parser.add_argument("--rerun-enumerations", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    files, pairs = verify_archive(args.archive)
    result = {"archive_sha256": ZIP_HASH, "archive_bytes": 920596, "archive_members": 28,
              "verified_member_hashes": 27, "candidate_sha256": PAIR_HASH,
              "decimal_verification": check_decimal(pairs),
              "enumeration_source_sha256": {name: sha(files[name]) for name in (
                  "valuation/lattice/lattice.cpp", "valuation/floor-sum/scan.cpp")},
              "checker_sha256": sha(Path(__file__).read_bytes())}
    if args.rerun_enumerations:
        require(not args.lattice_output and not args.floor_output, "choose fresh or supplied outputs")
        result["enumerations"] = rerun(files, pairs)
    else:
        result["enumerations"] = {"mode": "provided_outputs_verified" if args.lattice_output or
                                  args.floor_output else "not_rerun",
                                  "outputs": compare_outputs(pairs, args.lattice_output, args.floor_output)}
    serialized = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(serialized)
    print(serialized, end="")


if __name__ == "__main__":
    main()
