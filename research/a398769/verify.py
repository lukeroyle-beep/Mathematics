"""Reproduce the published A049102 baseline and both A398769 searches."""
from hashlib import sha256
from math import prod
from pathlib import Path
import subprocess
import tempfile

from by_multiset import candidates

HERE = Path(__file__).resolve().parent
TABLE_HASH = "368a7329f48e3dfa16a91a437d9f53af3291152c72a296a12500b516ad7127c9"


def require(ok, message):
    if not ok:
        raise SystemExit(message)


def qualifies(n):
    digits = list(map(int, str(n)))
    divisor = sum(digits) * prod(digits)
    return divisor > 0 and n % divisor == 0


def run_cpp(source, limit, build):
    binary = build / source
    subprocess.run(["c++", "-std=c++17", "-O3", "-Wall", "-Wextra", "-pedantic",
                    str(HERE / (source + ".cpp")), "-o", str(binary)], check=True)
    return subprocess.check_output([str(binary), str(limit)])


def main():
    with tempfile.TemporaryDirectory() as tmp:
        build = Path(tmp)
        baseline = run_cpp("parent", 14, build).replace(b"\r\n", b"\n")
        require(sha256(baseline).hexdigest() == TABLE_HASH, "Published b-file hash mismatch")
        rows = [list(map(int, row.split())) for row in baseline.splitlines()]
        require(len(rows) == 19637, "Unexpected number of published rows")
        terms = [n for _, n in rows]
        require(all(qualifies(n) for n in terms), "Invalid parent term")
        small = [n for n in range(1, 10**6) if qualifies(n)]
        require([n for n in terms if n < 10**6] == small, "Brute force disagrees below 10^6")
        odd = [n for n in terms if n % 2]
        require(len(odd) == 52 and all("1" in str(n) for n in odd), "Odd baseline mismatch")
        print("Published table reproduced: 19,637 terms, including 52 odd terms.", flush=True)

        # With 1 allowed, independent quotient enumeration must recover real
        # hits; this detects implementations that silently return no results.
        odd_alphabet = (1, 3, 5, 7, 9)
        for length in (1, 3, 5):
            reference = {n for n in odd if len(str(n)) == length}
            actual = {n for n, _, _ in candidates(length, odd_alphabet)}
            require(actual == reference, f"Positive control failed at length {length}")

        # Both factors divide this number individually, while their product does not.
        n = 357937935933375
        digits = list(map(int, str(n)))
        s, p = sum(digits), prod(digits)
        require(n % s == 0 and n % p == 0 and (n // p) % s == 76 and not qualifies(n),
                "Separate-divisibility regression failed")

        suffix_result = run_cpp("suffix_check", 19, build)
        require(suffix_result.decode().splitlines() ==
                (HERE / "suffix_check_19.csv").read_text().splitlines(),
                "Suffix traversal disagrees with recorded counts")
        print("Suffix traversal reproduced the counts at every odd length through 19.", flush=True)

        for length in range(1, 20, 2):
            hits = list(candidates(length))
            require(not hits, f"Independent quotient search found candidate(s): {hits}")
        print("Independent quotient search: zero counterexamples through 19 digits.")
        print("Even lengths are impossible, so this covers all positive n < 10^20.")


if __name__ == "__main__":
    main()
