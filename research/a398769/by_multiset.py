"""Search for A398769 counterexamples, using exact Python integers."""

from itertools import combinations_with_replacement
from math import gcd, prod

DIGITS = (3, 5, 7, 9)


def candidates(length, alphabet=DIGITS):
    """Generate hits of this length from a sorted alphabet of nonzero digits."""
    for digits in combinations_with_replacement(alphabet, length):
        digit_sum = sum(digits)
        digit_product = prod(digits)
        divisor = digit_sum * digit_product
        ordered = list(map(str, digits))
        low = int("".join(ordered))
        high = int("".join(reversed(ordered)))
        first_q = (low + divisor - 1) // divisor
        last_q = high // divisor
        if first_q > last_q:
            continue

        # For n = q * divisor, its units digit belongs to the multiset
        # and n is congruent to the digit sum modulo 9. Modulo 90
        # captures both tests. The residues repeat after this many q.
        period = 90 // gcd(90, divisor)
        for residue in range(period):
            representative = residue * divisor
            if representative % 10 not in digits or representative % 9 != digit_sum % 9:
                continue
            start = first_q + (residue - first_q) % period
            for q in range(start, last_q + 1, period):
                number = divisor * q
                if sorted(str(number)) == ordered:
                    yield number, digit_sum, digit_product


def main():
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("max_length", type=int, nargs="?", default=19)
    args = parser.parse_args()
    if args.max_length < 1:
        parser.error("max_length must be positive")
    for length in range(1, args.max_length + 1, 2):
        hits = list(candidates(length))
        for number, digit_sum, digit_product in hits:
            print(f"hit {number} sum={digit_sum} product={digit_product} "
                  f"quotient={number // (digit_sum * digit_product)}")
        print(f"{length} digits: {len(hits)} hits", flush=True)


if __name__ == "__main__":
    main()
