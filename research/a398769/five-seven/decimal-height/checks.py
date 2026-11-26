#!/usr/bin/env python3
"""Exact, bounded controls for the decimal-height investigation.

No floating logarithms, dense huge powers of ten, inherited checker imports,
or assert statements are used. Run from any directory; JSON is written to
stdout, or to --output. This is a finite check, not a proof of the global bound.
"""

import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import random


B = 1_000_002_000_000
BASE = "aab83fc4ed706cd4aca4d51dc6e533d60cb87477"
HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sign(n):
    return (n > 0) - (n < 0)


def sparse_sign(terms):
    """Sign of sum(c*10**e), using only short-gap dense powers.

    After collecting equal exponents, let c*10**e be the top term and f
    the next exponent. All lower terms have absolute sum at most A*10**f,
    A=sum(abs(coefficients)). If abs(c)*10**(e-f)>A, c determines the
    sign. Otherwise merge the top two terms. Since c is a nonzero integer,
    a merge requires e-f <= digits(A), so huge exponents are never expanded.
    """
    coefficients = {}
    for coefficient, exponent in terms:
        require(isinstance(coefficient, int) and isinstance(exponent, int)
                and exponent >= 0, "sparse integer domain")
        coefficients[exponent] = coefficients.get(exponent, 0) + coefficient
    rows = sorted(((e, c) for e, c in coefficients.items() if c), reverse=True)
    while len(rows) > 1:
        e, c = rows[0]
        f, q = rows[1]
        A = sum(abs(x[1]) for x in rows[1:])
        gap = e-f
        if gap >= len(str(A)):
            return sign(c)  # 10**gap>A, including exact decimal boundaries.
        shifted = c*10**gap
        if abs(shifted) > A:
            return sign(c)
        merged = shifted+q
        rows = ([(f, merged)] if merged else []) + rows[2:]
    return sign(rows[0][1]) if rows else 0


def fmod(L, i, modulus):
    return (7*pow(10, L, modulus)-18*pow(10, i, modulus)-25) % modulus


def valuation(n, prime):
    require(n != 0, "finite valuation")
    t = 0
    while n % prime == 0:
        t += 1
        n //= prime
    return t


def exact_depth(L, i, guard):
    """A bounded computation: fail explicitly if its guard is insufficient."""
    modulus = 7
    for t in range(guard):
        residue = fmod(L, i, modulus)
        if residue:
            require(residue % (modulus//7) == 0, "exact depth residue")
            return t, residue
        modulus *= 7
    raise ValueError(f"unresolved valuation by explicit guard {guard}")


def band(L):
    K, T = 1, 6
    while T <= L:
        K, T = K+1, 7*T
    return K, T


def representative(L, K, child_oracle=False):
    r, T, modulus = 3, 6, 7
    digits = []
    require(fmod(L, r, modulus) == 0, "initial representative")
    for j in range(1, K):
        residue = fmod(L, r, 7*modulus)
        require(residue % modulus == 0, "known lift depth")
        a = 5*(residue//modulus) % 7
        if child_oracle:
            children = [r+b*T for b in range(7)
                        if fmod(L, r+b*T, 7*modulus) == 0]
            require(children == [r+a*T], "independent seven-child lift")
        r += a*T
        digits.append(a)
        T, modulus = 7*T, 7*modulus
        require(0 <= r < T and fmod(L, r, modulus) == 0,
                "lifted representative")
    return r, digits


def quotient_digits(L, i):
    """Digits of floor(F/(225S)); for sum-compatible pairs this is digits(H).

    Binary search exact inequalities; only coefficients, not 10**L, are stored.
    The loop's upper endpoint is strict because F<7*10**L<225S*10**L.
    """
    S = 7*L-4
    terms = [(7, L), (-18, i), (-25, 0)]
    require(sparse_sign(terms + [(-225*S, 0)]) >= 0, "positive quotient")
    lo, hi = 0, L
    while hi-lo > 1:
        mid = (lo+hi)//2
        if sparse_sign(terms + [(-225*S, mid)]) >= 0:
            lo = mid
        else:
            hi = mid
    require(sparse_sign(terms + [(-225*S, hi-1)]) >= 0
            and sparse_sign(terms + [(-225*S, hi)]) < 0,
            "exact decimal bracket")
    return hi


def target_sign(L, i, t):
    # Positive or zero means 225S*10**t <= 10**12*F.
    return sparse_sign([(7, L+12), (-18, i+12), (-25, 12),
                        (-225*(7*L-4), t)])


def append_blocks(left, right, modulus):
    # Each block is (value modulo modulus, ten-to-length modulo modulus).
    return ((left[0]*right[1]+right[0]) % modulus,
            left[1]*right[1] % modulus)


def repeated_sevens(length, modulus):
    result, power = (0, 1 % modulus), (7 % modulus, 10 % modulus)
    while length:
        if length % 2:
            result = append_blocks(result, power, modulus)
        power = append_blocks(power, power, modulus)
        length //= 2
    return result


def word_mod(L, i, modulus):
    word = repeated_sevens(L-i-1, modulus)
    for block in ((5 % modulus, 10 % modulus),
                  repeated_sevens(i-1, modulus), (5 % modulus, 10 % modulus)):
        word = append_blocks(word, block, modulus)
    return word[0]


def comparator_controls():
    rng = random.Random(398769)
    tests = 0
    for _ in range(10_000):
        terms = [(rng.randrange(-10**8, 10**8), rng.randrange(0, 151))
                 for __ in range(rng.randrange(1, 10))]
        dense = sum(c*10**e for c, e in terms)
        require(sparse_sign(terms) == sign(dense), "sparse/dense sign")
        tests += 1
    # Exact cancellation and borrowing across gaps, including huge exponents.
    for e in (0, 1, 12, B, 10**100):
        for delta in (-1, 0, 1):
            require(sparse_sign([(1, e+1), (-10, e), (delta, 0)])
                    == sign(delta), "power-ten equality control")
            require(sparse_sign([(1, e+10), (-10**10+delta, e)])
                    == sign(delta), "coefficient-boundary control")
            tests += 2
    boundaries = 0
    for d in range(1, 101):
        for H in sorted({10**(d-1), 10**d-1, (10**d+10**(d-1))//2}):
            require(len(str(H)) == d, "boundary H digit count")
            for t in (0, d+10, d+11, d+12, d+13):
                require((10**t <= 10**12*H) == (t <= d+11),
                        "digit criterion exact endpoint")
                boundaries += 1
    H, t = 7**100, 100
    require(valuation(H, 7) == t and 10**t > 10**12*H,
            "generic positive integer countercontrol")
    return dict(sparse_dense_and_boundary_comparisons=tests,
                digit_criterion_comparisons=boundaries,
                generic_integer_failure_control=dict(H="7^100", t=t,
                                                     d=len(str(H)),
                                                     is_F_cofactor_claim=False))


def small_controls():
    pairs = compatible = divisible_by_three = 0
    depths = Counter()
    positive_examples = []
    for L in range(5, 302, 2):
        S, K = 7*L-4, band(L)[0]
        r, _ = representative(L, K, child_oracle=True)
        for i in range(3, L):
            word = "7"*(L-i-1)+"5"+"7"*(i-1)+"5"
            n = int(word)
            F = 7*10**L-18*10**i-25
            P = 1
            for digit in word:
                P *= int(digit)
            require(9*n == F and sum(map(int, word)) == S
                    and P == 25*7**(L-2), "original decimal definition")
            require((n % (P*S) == 0) == (F % (225*S*7**(L-2)) == 0),
                    "original full witness equivalence")
            require(valuation(F, 5) == 2, "suffix five valuation")
            t = valuation(F, 7)
            require(t < K or i == r, "actual position uniqueness")
            if t < K:
                require(225*S*10**t < F, "strong low-depth size replacement")
            if S % 5 and F % (9*S) == 0:
                H = F//(225*S)
                require(F % (225*S) == 0 and H > 0
                        and valuation(H, 7) == t, "integral cofactor")
                d = quotient_digits(L, i)
                require(d == len(str(H)), "sparse quotient digit count")
                require((target_sign(L, i, t) >= 0) == (10**t <= 10**12*H)
                        == (t <= d+11), "target three-way exact comparison")
                require(t <= d+11, "small target")
                require((F % 7**(d+12) == 0) == (10**t > 10**12*H),
                        "failure exactly depth d+12")
                compatible += 1
                divisible_by_three += S % 3 == 0
                depths[t] += 1
                if len(positive_examples) < 6:
                    positive_examples.append(dict(L=L, i=i, S=S, t=t, d=d))
            for modulus in (9*S, 7**(t+1)):
                require(word_mod(L, i, modulus) == n % modulus,
                        "block concatenation versus literal word")
            pairs += 1
    L, i = 313, 51
    S = 7*L-4
    require(S % 3 == 0 and fmod(L, i, S) == 0 and fmod(L, i, 9*S) != 0,
            "factor nine negative control")
    return dict(odd_lengths_inclusive=[5, 301], positions="all 3 <= i < L",
                pairs=pairs, sum_compatible_five_free_pairs=compatible,
                sum_compatible_pairs_with_3_dividing_S=divisible_by_three,
                depth_histogram=dict(sorted(depths.items())),
                examples=positive_examples,
                factor_nine_negative_control=dict(L=L, i=i, S=S,
                    F_mod_S=fmod(L, i, S), F_mod_9S=fmod(L, i, 9*S)))


def sampled_lengths():
    # Explicit scattered samples, rather than an attempted exhaustive extension.
    lengths = {B+1+2*q*q for q in range(128)}
    for k in range(16, 65):
        lengths.update((6*7**(k-2)+1, 6*7**(k-1)-1))
    return sorted(L for L in lengths if L > B and (7*L-4) % 5)


def high_position_diagnostics():
    rows, actual, sum_positive, max_depth = [], 0, 0, 0
    for L in sampled_lengths():
        S = 7*L-4
        K, T = band(L)
        r, digits = representative(L, K)
        row = dict(L=str(L), K=K, r_K=str(r), actual=3 <= r < L)
        require(T > L and T//7 <= L, "K band")
        if row["actual"]:
            actual += 1
            residue_sum = fmod(L, r, 9*S)
            t, residue_next = exact_depth(L, r, K+32)
            require(t >= K, "actual depth K")
            lifted, all_digits = representative(L, t+1)
            require(all(a == 0 for a in all_digits[K-1:t-1])
                    and all_digits[t-1] != 0 and lifted >= L,
                    "inclusive first nonzero lift index")
            d = quotient_digits(L, r)
            require(target_sign(L, r, t) >= 0 and t <= d+11,
                    "sample actual target")
            require(d+11 <= L-3, "sample witness deadline")
            require(9*word_mod(L, r, 7**(t+1)) % 7**(t+1) == residue_next,
                    "sample original-word valuation")
            sum_positive += residue_sum == 0
            max_depth = max(max_depth, t)
            row.update(F_mod_9S=str(residue_sum), t=t, d=str(d),
                       F_mod_7_next=str(residue_next), inequality=True,
                       sum_compatible=residue_sum == 0)
        rows.append(row)
    return dict(scope="all sum-compatible positions at each listed sampled length, using the proved t<K size bound and the unique r_K for t>=K",
                sample_definition="five-free lengths >B in {B+1+2*q^2:0<=q<=127} union {6*7^(k-2)+1,6*7^(k-1)-1:16<=k<=64}",
                sampled_lengths=len(rows), actual_r_K_count=actual,
                sum_compatible_r_K_count=sum_positive, maximum_actual_depth=max_depth,
                valuation_guard="K+32; raises without a result if exhausted",
                rows=rows)


def giant_positive_controls():
    # Retained inputs, freshly checked by powers and separate original-word blocks.
    inputs = [HERE.parent/"fixed-depth/checks.json",
              HERE.parent/"trillion-witness/families/results.json"]
    fixed = json.loads(inputs[0].read_text())["appendix_examples"]
    family = json.loads(inputs[1].read_text())["rows"][0]
    pairs = [(int(row["L"]), int(row["i"]), "fixed-depth appendix") for row in fixed]
    pairs += [(int(family["L"]), int(family["first_position"]), "family t=0 first position")]
    pairs += [(int(family["L"]), int(row["i"]), "family t=0 deepest position")
              for row in family["deepest_positions"]]
    rows = []
    for L, i, origin in pairs:
        S = 7*L-4
        require(L > B and L % 2 and 3 <= i < L and S % 5 and S % 3 == 0,
                "giant sum-control domain including 3|S")
        require(fmod(L, i, 225*S) == 0 and word_mod(L, i, 25*S) == 0,
                "giant full-sum positive control")
        K = band(L)[0]
        t, residue = exact_depth(L, i, K+32)
        d = quotient_digits(L, i)
        require(target_sign(L, i, t) >= 0 and t <= d+11 <= L-3,
                "giant target and deadline")
        require(9*word_mod(L, i, 7**(t+1)) % 7**(t+1) == residue,
                "giant original-word exact depth")
        require(t < L-2, "giant full witness rejected")
        rows.append(dict(origin=origin, L=str(L), i=str(i), S=str(S), K=K,
                         t=t, d=str(d), F_mod_225S=0, n_mod_25S=0,
                         F_mod_7_next=str(residue), inequality=True,
                         full_witness=False))
    require(any(row["t"] == 0 for row in rows)
            and any(row["t"] > 0 for row in rows), "nonzero and zero depth controls")
    return dict(inputs=[dict(path=str(path.relative_to(HERE.parent)),
                             sha256=sha256(path.read_bytes()).hexdigest())
                        for path in inputs],
                positions=len(rows), rows=rows,
                scope="only these six actual positions; family enumeration not rerun")


def endpoint_controls():
    cutoff = (7*10**14+899)//1575  # integer L with 1575L-900<7*10**14
    require(cutoff == 444_444_444_445 and cutoff < B,
            "independent strict integer cutoff")
    require(225*(7*cutoff-4) < 7*10**14
            and 225*(7*(cutoff+1)-4) >= 7*10**14, "cutoff neighbors")
    # For L>=9, 225S<10**(floor(L/2)+1), by two-step induction.
    for L in (9, 10):
        require(225*(7*L-4) < 10**(L//2+1), "size induction base")
    # 10*(7L-4)-(7(L+2)-4)=63L-50>0 for L>=1.
    require(63*1-50 > 0, "size induction recurrence base")
    # K<=ceil(L/2): period base at 5,6; a two-step increase multiplies T by 7.
    for L in (5, 6):
        require(6*7**((L+1)//2-1) > L, "half-length period base")
    for L in range(5, 9):
        K = band(L)[0]
        require(225*(7*L-4)*10**(K-1) < 52*10**(L-1)-25,
                "short low-depth cases")
    # T_(L-2)>L already for L=5; its ratio 7 exceeds (L+1)/L.
    require(6*7**2 > 5, "period induction base")
    # For L>B, F/(225S)<10^(L-14), strictly, hence d+11<=L-3.
    require(225*(7*(B+1)-4) > 7*10**14, "deadline base beyond B")
    return dict(inclusive_full_witness_cutoff=cutoff,
                next_integer_fails_strict_cutoff=cutoff+1,
                first_remaining_odd=B+1, K_at_first_remaining=band(B+1)[0],
                d_plus_11_upper_bound="L-3 for every L>B",
                low_depth_size_bound="t<K => 10^t<F/(225S), for every L>=5, 3<=i<L")


def zero_lift_control():
    L, i = 69489, 40323
    K = band(L)[0]
    r, _ = representative(L, K, child_oracle=True)
    t, residue = exact_depth(L, i, 40)
    escaped, digits = representative(L, t+1, child_oracle=True)
    require(r == i and K == 6 and t == 11 and residue == 5*7**11,
            "zero-run exact valuation control")
    require(digits[K-1:t-1] == [0]*5 and digits[t-1] == 4 and escaped > L,
            "zero-run endpoints K through t-1 then a_t")
    require(fmod(L, i, 9*(7*L-4)) == 2218743, "zero-run sum failure control")
    return dict(L=L, i=i, K=K, t=t, zero_indices_inclusive=[6, 10],
                first_nonzero_index=11, first_nonzero_digit=4,
                F_mod_7_next=residue, F_mod_9S=2218743,
                scope="lift control only; sum premise fails")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    receipt = dict(status="PASS: finite exact checks only", starting_main=BASE,
                   source_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
                   comparator_controls=comparator_controls(),
                   endpoint_controls=endpoint_controls(),
                   zero_lift_control=zero_lift_control(),
                   small_controls=small_controls(),
                   sampled_lengths=high_position_diagnostics(),
                   giant_positive_controls=giant_positive_controls(),
                   limitations=["No global inequality proof or refutation.",
                                "No new exhaustive consecutive interval above B claimed.",
                                "No full witness found; no Lean theorem or build.",
                                "The inherited trillion and million-length enumerations were not rerun."])
    output = json.dumps(receipt, indent=2, sort_keys=True)+"\n"
    if args.output:
        args.output.write_text(output)
    else:
        print(output, end="")


if __name__ == "__main__":
    main()
