#!/usr/bin/env python3
"""Independent literal predicate, primary coverage, and compiled arithmetic controls."""
import csv
import hashlib
import json
from math import gcd, prod
from pathlib import Path
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent


def require(ok, message):
    if not ok:
        raise ArithmeticError(message)


def word_mod(L, i, m):
    """Concatenate the original decimal blocks, without division or sparse F."""
    def sevens(n):
        value, shift, block, width = 0, 1, 7 % m, 10 % m
        while n:
            if n & 1:
                value, shift = (value * width + block) % m, shift * width % m
            block, width = block * (width + 1) % m, width * width % m
            n //= 2
        return value, shift
    prefix, _ = sevens(L-i-1)
    middle, shift = sevens(i-1)
    return ((10*prefix+5)*shift*10+middle*10+5) % m


def main():
    direct, positive, singular, boundary_h = 0, 0, 0, set()
    stream = hashlib.sha256()
    # The original problem predicate has a nonzero positive control.
    for text, expected in (("135", True), ("137", False)):
        digits = list(map(int, text))
        require((int(text) % (prod(digits)*sum(digits)) == 0) == expected,
                "original product-times-sum control")
    with tempfile.TemporaryDirectory(prefix="a398769-controls-") as directory:
        temp = Path(directory)
        binary = temp / "primary"
        subprocess.run(["clang++", "-O3", "-std=c++17", str(HERE / "primary.cpp"),
                        "-o", str(binary)], check=True)
        for b in list(range(2, 17)) + [50, 51]:
            by_depth = {depth: [] for depth in range(1, 5)}
            for L in range(5, 502, 2):
                for i in range(3, L, 6):
                    text = "7"*(L-i-1) + "5" + "7"*(i-1) + "5"
                    n, S, P = int(text), sum(map(int, text)), prod(map(int, text))
                    F = 7*10**L - 18*10**i - 25
                    require((9*n, S, P) == (F, 7*L-4, 25*7**(L-2)), "decimal identity")
                    require((n % (P*S) == 0) == (F % (225*S*7**(L-2)) == 0), "full divisor")
                    require(word_mod(L, i, S) == n % S, "decimal block evaluator")
                    for a in range(1, b):
                        h = b*i-a*L
                        if gcd(a, b) != 1 or abs(h) > 16:
                            continue
                        for depth in range(1, 5):
                            if (9*n) % 7**depth == 0:
                                by_depth[depth].append((a, h, L, i))
            for at in range(1, 5):
                expected = sorted(by_depth[at])
                command = [str(binary), "--K", "4", "--b", str(b), "--lo", "5", "--hi", "501",
                           "--depth", "4", "--at", str(at), "--pairs", str(temp / "pairs.csv"),
                           "--pairs22", str(temp / "deep.csv"), "--json", str(temp / "counts.json")]
                subprocess.run(command, check=True)
                actual = [tuple(map(int, row)) for row in csv.reader((temp / "pairs.csv").open())]
                deep = [tuple(map(int, row)) for row in csv.reader((temp / "deep.csv").open())]
                record = json.loads((temp / "counts.json").read_text())
                require(actual == expected, f"complete literal enumeration b={b} at={at}")
                require(deep == sorted(by_depth[4]), "all continued children to terminal depth")
                free = [(L, i) for _, _, L, i in actual if (7*L-4) % 5]
                sums = sum(word_mod(L, i, 7*L-4) == 0 for L, i in free)
                require(record["fivefree13"] == len(free) and record["sum13"] == sums,
                        "full nine digit sum")
                direct += len(actual)
                positive += sums
                singular += sum(a % 7 == 0 and at >= 2 for a, h, L, i in actual)
                boundary_h.update(h for a, h, L, i in actual if h in (-16, 0, 16))
                stream.update((temp / "pairs.csv").read_bytes())
        require(positive and singular and boundary_h == {-16, 0, 16}, "nonvacuous controls")
        # Nonzero depth22 arithmetic, full-sum positives incl. 3|S, and lost-nine negative.
        # The deep pair is only a control; no inherited search is being rerun here.
        cases = [(2016691727, 428102277), (61, 57), (165, 33), (313, 51)]
        require(word_mod(*cases[0], 7**22) == 0, "depth22 positive from original word")
        require(word_mod(61, 57, 423) == 0, "composite full-sum positive")
        require(word_mod(313, 51, 2187) != 0, "factor-nine negative")
        require((9*word_mod(313, 51, 2187)) % 2187 == 0, "lost-nine trap")
        arithmetic = []
        for source, expression in (("primary.cpp", "residue(power(10,L,m),power(10,i,m),m)"),
                                   ("independent.cpp", "F(power(10,L,m),power(10,i,m),m)")):
            harness = temp / "harness.cpp"
            code = '#define main enumeration_entry\n#include "' + str(HERE/source) + '"\n#undef main\n'
            code += 'int main(){\n'
            for L, i in cases:
                for m in (7**22, 7**21, 9*(7*L-4), 7*L-4):
                    code += f'{{ U L={L}ULL,i={i}ULL,m={m}ULL; std::cout << {expression} << "\\n"; }}\n'
            code += 'return 0;}\n'
            harness.write_text(code)
            subprocess.run(["clang++", "-O2", "-std=c++17", str(harness), "-o", str(temp/"harness")], check=True)
            values = list(map(int, subprocess.check_output([str(temp/"harness")], text=True).splitlines()))
            expected = [(9*word_mod(L, i, m)) % m for L, i in cases
                        for m in (7**22, 7**21, 9*(7*L-4), 7*L-4)]
            require(values == expected, source + " compiled arithmetic vs original concatenation")
            arithmetic.append({"source": source, "comparisons": len(values)})
        # Singleton intervals retain either endpoint, including an actual depth13 root.
        for L, i, k, b, a, h in ((9, 3, 4, 2, 1, -3),
                                 (40932783702951, 141635929767, 17, 289, 1, -288)):
            at = 1 if L == 9 else 13
            subprocess.run([str(binary), "--K", str(k), "--b", str(b), "--lo", str(L), "--hi", str(L),
                            "--at", str(at), "--pairs", str(temp/"pairs.csv"),
                            "--pairs22", str(temp/"deep.csv"), "--json", str(temp/"counts.json")], check=True)
            actual = [tuple(map(int, row)) for row in csv.reader((temp/"pairs.csv").open())]
            require((a, h, L, i) in actual, "inclusive singleton positive")
    print(json.dumps({"status": "PASS", "direct_partitions": 68, "direct_pair_occurrences": direct,
                      "positive_sum_occurrences": positive, "singular_positive_occurrences": singular,
                      "offset_endpoints_and_zero": sorted(boundary_h), "stream_sha256": stream.hexdigest(),
                      "compiled_original_decimal_comparisons": arithmetic,
                      "depth22_positive": list(cases[0]), "original_PS_positive": 135,
                      "source_sha256": {name: hashlib.sha256((HERE/name).read_bytes()).hexdigest()
                                        for name in ("primary.cpp", "independent.cpp")}}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
