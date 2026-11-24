"""Compare both Stage 5 searches with direct arithmetic and reject bad CLI input."""

import ast
import contextlib
import io
import itertools
import runpy
import subprocess
import sys
from math import comb, prod
from pathlib import Path


def direct_hits(words):
    """Return exact (number, digit sum, digit product, quotient) rows."""
    hits = set()
    for word in words:
        digits = tuple(map(int, word))
        number = int("".join(map(str, digits)))
        digit_sum, digit_product = sum(digits), prod(digits)
        quotient, remainder = divmod(number, digit_sum * digit_product)
        if remainder == 0:
            hits.add((number, digit_sum, digit_product, quotient))
    return hits


def check_prefix(executable, length, expected, multiset=None):
    args = [str(executable), str(length)]
    if multiset is not None:
        args += ["--multiset", multiset]
    output = subprocess.check_output(args, text=True)
    rows = []
    for line in output.splitlines():
        if line.startswith("hit "):
            rows.append(tuple(int(field.split("=")[-1]) for field in line.split()[1:]))
    assert len(rows) == len(set(rows)), (args, "duplicate hits")
    assert set(rows) == expected, (args, rows, expected)
    summary = dict(field.split("=") for field in output.splitlines()[-1].split())
    assert int(summary["length"]) == length
    assert int(summary["multisets"]) == (1 if multiset is not None else comb(length + 3, 3))
    assert int(summary["hits"]) == len(expected)


def check_quotient(search, length, width, expected, multiset=None):
    stream = io.StringIO()
    with contextlib.redirect_stdout(stream):
        search(length, width, restricted=multiset, perform=True)
    fields = stream.getvalue().strip().split(maxsplit=4)
    assert len(fields) == 5, stream.getvalue()
    assert tuple(map(int, fields[:3])) == (
        length, width, 1 if multiset is not None else comb(length + 3, 3)
    )
    hits = ast.literal_eval(fields[4])
    assert len(hits) == len(set(hits)), (length, width, multiset, "duplicate hits")
    assert set(hits) == {row[0] for row in expected}, (length, width, multiset, hits, expected)
    assert int(fields[3]) >= len(hits)


def check_rejections(executable, quotient):
    prefix_cases = [[], ["0"], ["24"], ["3x"], ["3", "--unknown"],
                    ["3", "--multiset", "11"], ["3", "--multiset", "132"]]
    quotient_cases = [[], ["0", "1"], ["24", "1"], ["3", "0"], ["3", "4"],
                      ["3x", "1"], ["3", "x"], ["3", "1", "--unknown"],
                      ["3", "1", "--multiset=11"], ["3", "1", "--multiset=132"],
                      ["3", "1", "--multiset="]]
    for command, cases in (([str(executable)], prefix_cases),
                           ([sys.executable, str(quotient)], quotient_cases)):
        for args in cases:
            result = subprocess.run(command + args, capture_output=True, text=True)
            assert result.returncode == 2, (command, args, result.returncode, result.stderr)
            assert not result.stdout.strip(), (command, args, result.stdout)
    return len(prefix_cases) + len(quotient_cases)


def check_count_only(quotient):
    # A known positive case must not look like a completed zero-hit search.
    command = [sys.executable, str(quotient), "3", "1", "--multiset=135"]
    counted = subprocess.check_output(command, text=True).strip().split(maxsplit=4)
    checked = subprocess.check_output(command + ["--run"], text=True).strip().split(maxsplit=4)
    assert counted[:4] == checked[:4]
    assert counted[4] == "NOT_CHECKED"
    assert ast.literal_eval(checked[4]) == [135]


def main():
    executable = Path(sys.argv[1]).resolve()
    quotient = Path(__file__).with_name("quotient23.py")
    search = runpy.run_path(str(quotient))["search"]
    prefix_checks = quotient_checks = 0

    for length in range(1, 8):
        expected = direct_hits(itertools.product("3579", repeat=length))
        check_prefix(executable, length, expected)
        prefix_checks += 1
        for width in sorted({1, min(3, length), length}):
            check_quotient(search, length, width, expected)
            quotient_checks += 1
    print("Full {3,5,7,9} alphabet agrees with direct enumeration at lengths 1 through 7.")

    # All small odd-digit multisets include positive controls such as 135,
    # whose divisor is divisible by both 5 and 9, exercising both gcd filters.
    multisets = 0
    for length in range(1, 6):
        for digits in itertools.combinations_with_replacement("13579", length):
            multiset = "".join(digits)
            expected = direct_hits(set(itertools.permutations(digits)))
            check_prefix(executable, length, expected, multiset)
            prefix_checks += 1
            for width in sorted({1, min(3, length), length}):
                check_quotient(search, length, width, expected, multiset)
                quotient_checks += 1
            multisets += 1
    assert multisets == 251
    print("All 251 odd-digit multisets at lengths 1 through 5 agree, at multiple suffix widths.")

    words = []
    for positions in itertools.combinations(range(23), 2):
        digits = [1] * 23
        for position in positions:
            digits[position] = 3
        words.append(digits)
    assert len(words) == 253
    expected = direct_hits(words)
    assert len(expected) == 10
    assert all(row[0] > 2**64 for row in expected)
    multiset = "1" * 21 + "33"
    check_prefix(executable, 23, expected, multiset)
    check_quotient(search, 23, 21, expected, multiset)
    prefix_checks += 1
    quotient_checks += 1
    print("23-digit control: all 253 placements checked; both searches give the same ten exact hits.")

    rejected = check_rejections(executable, quotient)
    check_count_only(quotient)
    print(f"Passed {prefix_checks} prefix checks, {quotient_checks} quotient checks, "
          f"{rejected} invalid-command checks, and the count-only CLI check.")


if __name__ == "__main__":
    main()
