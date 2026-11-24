"""Compare the prefix search with direct decimal arithmetic on known cases."""
import itertools
import subprocess
import sys
from math import prod
from pathlib import Path


def fields_if_hit(digits):
    number = int("".join(map(str, digits)))
    digit_sum, digit_product = sum(digits), prod(digits)
    quotient, remainder = divmod(number, digit_sum * digit_product)
    if remainder == 0:
        return number, digit_sum, digit_product, quotient
    return None


def verify(executable, args, expected):
    output = subprocess.check_output([str(executable), *args], text=True)
    rows = []
    for line in output.splitlines():
        if line.startswith("hit "):
            fields = line.split()[1:]
            rows.append(tuple(int(field.split("=")[-1]) for field in fields))
    if len(rows) != len(set(rows)) or set(rows) != expected:
        raise SystemExit(f"Hit list mismatch for {args}: {rows}")
    return len(rows)


def main():
    executable = Path(sys.argv[1]).resolve()
    for length in range(1, 10):
        with_one, without_one = set(), set()
        for digits in itertools.product((1, 3, 5, 7, 9), repeat=length):
            hit = fields_if_hit(digits)
            if hit:
                with_one.add(hit)
                if 1 not in digits:
                    without_one.add(hit)
        verify(executable, [str(length)], without_one)
        verify(executable, [str(length), "--include-one"], with_one)
    print("Small controls agree for both alphabets at lengths 1 through 9.")

    # The full 21-digit control has only 21 distinct arrangements. Every
    # arrangement exceeds 2**64. The three hits exercise the wide integer path.
    expected = set()
    for index in range(21):
        digits = [1] * 21
        digits[index] = 7
        hit = fields_if_hit(digits)
        if hit:
            expected.add(hit)
    if len(expected) != 3:
        raise SystemExit("Direct 21-digit control did not give the expected three hits")
    verify(executable, ["21", "--multiset", "1" * 20 + "7"], expected)
    print("21-digit positive control: all three exact hits and quotients agree.")


if __name__ == "__main__":
    main()
