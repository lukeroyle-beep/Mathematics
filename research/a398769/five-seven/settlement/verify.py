#!/usr/bin/env python3
"""Rebuild the lifting sieve, cross-check decimal words, and write a receipt.

Python 3.8+, C++17 with unsigned __int128. Uses exact integers throughout.
The independent fixed-modulus program is a separate command.
"""
import argparse
from fractions import Fraction
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import platform
import subprocess
import tempfile
import time

HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def decimal_pair(length, position):
    # Actual decimal construction, independent of the formula for F.
    digits = [7] * length
    digits[0] = digits[position] = 5
    n, p = 0, 1
    for digit in reversed(digits):
        n = 10 * n + digit
        p *= digit
    return n, p, sum(digits)


def small_checks(binary):
    direct = {}
    pairs = 0
    full_survivors = []
    for length in range(5, 302, 2):
        direct[length] = {}
        for position in range(3, length, 6):
            n, p, s = decimal_pair(length, position)
            f = 7*10**length - 18*10**position - 25
            require(9*n == f, "decimal reconstruction")
            require(p == 25*7**(length-2) and s == 7*length-4, "digit P,S")
            require((n % (p*s) == 0) == (f % (9*p*s) == 0), "full divisor")
            direct[length][position] = n
            pairs += 1
            if n % (p*s) == 0:
                full_survivors.append([length, position])
    modular_comparisons = 0
    for cap in range(1, 6):
        result = json.loads(subprocess.check_output(
            [str(binary), "--max", "301", "--power", str(cap), "--residues"], text=True))
        require(len(result["residues"]) == len(direct), "small endpoint coverage")
        for length, residue, period in result["residues"]:
            k = min(cap, length-2)
            actual = [i for i, n in direct[length].items() if n % 7**k == 0]
            lifted = list(range(residue, length, period))
            require(lifted == actual, f"modular cross-check L={length},k={k}")
            modular_comparisons += 1
        # Exercise ordinary pruning and enumeration too, with nonempty controls.
        pruned = json.loads(subprocess.check_output(
            [str(binary), "--max", "301", "--power", str(cap)], text=True))
        expected = [[length, i] for length, entries in direct.items()
                    for i, n in entries.items() if n % 7**min(cap, length-2) == 0]
        require(pruned["truncated_7_power_survivors"] == expected, "pruned enumeration")
        if cap == 1:
            require(len(expected) == pairs > 0, "positive modular control")

    # All words in the original subclass, not only the positional reduction.
    words = 0
    for length in range(1, 16, 2):
        for digits in itertools.product((5, 7), repeat=length):
            n, p = 0, 1
            for digit in digits:
                n = 10*n + digit
                p *= digit
            require(n % (p*sum(digits)) != 0, "small original-family witness")
            words += 1
    require(words == 43690, "original word count")
    n, _, _ = decimal_pair(23, 15)
    require(9*n % 49 == 0 and 9*n % 343 == 245, "(23,15) regression")
    n45, _, _ = decimal_pair(51, 45)
    require(9*n45 % 49 == 0 and 45 in direct[51], "position 45 retained")
    require(not full_survivors, "small full-divisor survivors")
    # Every full-divisor filter is checked over its complete joint period.
    filter_counts = {}
    for prime, order, forbidden in [(11, 2, 10), (13, 6, 8), (37, 3, 27), (101, 4, 15)]:
        residues = {(7*pow(10, L, prime)-18*pow(10, i, prime)-25) % prime
                    for L in range(1, 6*order+1, 2) for i in range(3, 6*order+1, 6)}
        require(0 not in residues, "full-divisor prime filter")
        require((7*forbidden-4) % prime == 0, "forbidden length residue")
        filter_counts[str(prime)] = sorted(residues)
    require(775 % 25 == 0 and 775 % 125 != 0 and (7*2-4) % 5 == 0, "5-adic filter")
    return dict(decimal_pairs_through_301=pairs, modular_length_power_comparisons=modular_comparisons,
                all_original_words_through_15=words, full_divisor_survivors=full_survivors,
                regression_23_15_F_mod_49=0, regression_23_15_F_mod_343=245,
                position_45_modulo_49_control=[51, 45], prime_filter_F_residues=filter_counts)


def analytic_arithmetic():
    spec = importlib.util.spec_from_file_location("log_bounds", HERE.parent / "log_bounds.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    Q = Fraction
    lo7, _ = module.reduced_log_interval(Q(7, 4), 2)
    _, hi10 = module.reduced_log_interval(Q(5, 4), 3)
    require(168*hi10**2 / lo7**4 < 63, "edge prefactor")
    require(7*hi10 < 18, "log(10^7)<18")
    require(63*396*400 == 9979200 < 10000000-3, "plateau cutoff")
    require(126*396*20 == 997920 < 10000000, "derivative cutoff")
    return dict(prefactor_strictly_below=63, edge_parameter_max=395,
                plateau_bound=9979200, cutoff_length=10000000)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-length", type=int, default=10000000)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    require(5 <= args.max_length <= 100000000, "max length out of range")
    start = time.monotonic()
    with tempfile.TemporaryDirectory(prefix="a398769-lift-") as tmp:
        binary = Path(tmp) / "lift_sieve"
        command = ["c++", "-std=c++17", "-O3", "-Wall", "-Wextra", "-Wconversion",
                   str(HERE / "lift_sieve.cpp"), "-o", str(binary)]
        subprocess.run(command, check=True)
        checks = small_checks(binary)
        result = json.loads(subprocess.check_output(
            [str(binary), "--max", str(args.max_length), "--power", "20"], text=True))
    require(result["odd_lengths_checked"] == (args.max_length-3)//2, "global length count")
    # Any truncated survivors are tested with the growing power AND full divisor.
    tested = []
    for length, position in result["truncated_7_power_survivors"]:
        n, p, s = decimal_pair(length, position)
        q, remainder = divmod(n, p*s)
        weak = n % 7**(length-2) == 0
        require(n == q*p*s + remainder, "quotient reconstruction")
        tested.append(dict(L=length, i=position, growing_7_power=weak,
                           full_divisor=remainder == 0))
    require(sum(result["rejected_at_power"].values()) + len(tested)
            == result["odd_lengths_checked"], "rejection partition")
    receipt = dict(verdict="no candidates in the claimed finite range" if not tested
                   else "inspect full_candidate_tests", base_commit="66f9135254ec4f4dc58acfc6287170fff23e098a",
                   arithmetic="exact integers; no Lean checking", search=result,
                   small_checks=checks, analytic_constant_checks=analytic_arithmetic(),
                   full_candidate_tests=tested, python=platform.python_version(),
                   compiler=subprocess.check_output(["c++", "--version"], text=True).splitlines()[0],
                   elapsed_seconds=round(time.monotonic()-start, 3),
                   source_sha256={name: hashlib.sha256((HERE/name).read_bytes()).hexdigest()
                                  for name in ("lift_sieve.cpp", "verify.py")})
    text = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text)
    print(text, end="")


if __name__ == "__main__":
    main()
