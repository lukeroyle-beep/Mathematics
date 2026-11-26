#!/usr/bin/env python3
"""Independent review controls; no checker imports and no global search claim.

The decimal sign oracle propagates signed carries upward, unlike the
implementation's downward coefficient dominance. The word oracle evaluates
the repunit in modulus 9m and divides its representative by nine, so it also
works when 3 divides m. Representatives use seven-child enumeration rather
than the implementation's explicit lift coefficient.
"""
from collections import Counter
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
import random
import subprocess

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
REVIEWED = "574cd7a28357e7d4e94f1f47aae749732eb51078"
B = 1000002000000


def need(ok, why):
    if not ok:
        raise ValueError(why)


def carry_sign(terms):
    coefficients = {}
    for c, e in terms:
        need(isinstance(c, int) and isinstance(e, int) and e >= 0, "domain")
        coefficients[e] = coefficients.get(e, 0) + c
    rows = sorted(coefficients.items())
    if not rows:
        return 0
    e, c = rows[0]
    lower_nonzero = False
    for f, a in rows[1:]:
        gap = f-e
        if gap >= len(str(abs(c))):
            carry = -1 if c < 0 else 0
            remainder_nonzero = c != 0
        else:
            carry, remainder = divmod(c, 10**gap)
            remainder_nonzero = remainder != 0
        lower_nonzero |= remainder_nonzero
        e, c = f, a+carry
    return -1 if c < 0 else 1 if c > 0 or lower_nonzero else 0


def word_mod(L, i, modulus):
    repunit = (pow(10, L, 9*modulus)-1)//9
    return (7*repunit-2*pow(10, i, modulus)-2) % modulus


def depth_from_word(L, i, guard):
    value = word_mod(L, i, 7**guard)
    need(value != 0, "independent valuation guard exhausted")
    t = 0
    while value % 7 == 0:
        value //= 7
        t += 1
    return t


def digits_from_carries(L, i):
    D = 225*(7*L-4)
    q = len(str(D))
    cutoff = L-q+1
    comparison = carry_sign([(7, L), (-18, i), (-25, 0), (-D, cutoff)])
    return cutoff+(comparison >= 0)


def literal_controls():
    count = compatible = three = 0
    depths = Counter()
    for L in range(5, 302, 2):
        S = 7*L-4
        for i in range(3, L):
            digits = [5 if j in (0, i) else 7 for j in reversed(range(L))]
            n = 0
            product = 1
            for a in digits:
                n = 10*n+a
                product *= a
            F = 9*n
            need(sum(digits) == S and product == 25*7**(L-2), "literal digits")
            need(F == 7*10**L-18*10**i-25, "literal polynomial")
            need(word_mod(L, i, 25*S) == n % (25*S), "repunit modulo 25S")
            need(digits_from_carries(L, i) == len(str(F//(225*S))), "carry digits")
            if S % 5 and n % S == 0:
                need(n % (25*S) == 0, "integral cofactor including 3|S")
                H = n//(25*S)
                t = depth_from_word(L, i, L+1)
                d = len(str(H))
                need((10**t <= 10**12*H) == (t <= d+11), "digit equivalence")
                need((n % (product*S) == 0) == (t >= L-2), "full witness")
                need(t <= d+11, "literal target")
                compatible += 1
                three += S % 3 == 0
                depths[t] += 1
            count += 1
    return dict(pairs=count, sum_compatible=compatible, divisible_by_three=three,
                depth_histogram=dict(sorted(depths.items())))


def carry_controls():
    rng = random.Random(225398769)
    count = 0
    for _ in range(5000):
        terms = [(rng.randrange(-10**16, 10**16), rng.randrange(201))
                 for _ in range(rng.randrange(1, 12))]
        dense = sum(c*10**e for c, e in terms)
        need(carry_sign(terms) == (dense > 0)-(dense < 0), "signed carry oracle")
        count += 1
    for e in (0, 1, B, 10**100):
        for delta in (-1, 0, 1):
            need(carry_sign([(1, e+1), (-10, e), (delta, 0)]) == delta,
                 "huge exact cancellation")
            count += 1
    return count


def sample_controls(receipt):
    expected = {B+1+2*u*u for u in range(128)}
    expected.update(6*7**(k-2)+1 for k in range(16, 65))
    expected.update(6*7**(k-1)-1 for k in range(16, 65))
    expected = sorted(L for L in expected if L > B and (7*L-4) % 5)
    rows = receipt['sampled_lengths']['rows']
    need([int(row['L']) for row in rows] == expected, "exact scattered sample set")
    actual = maximum = sum_positive = 0
    for row in rows:
        L = int(row['L'])
        r, period, modulus, K = 3, 6, 7, 1
        while period <= L:
            modulus *= 7
            children = [r+a*period for a in range(7)
                        if word_mod(L, r+a*period, modulus) == 0]
            need(len(children) == 1, "seven-child uniqueness")
            r = children[0]
            period *= 7
            K += 1
        need(r == int(row['r_K']) and K == row['K'], "unseeded representative")
        need(row['actual'] == (3 <= r < L), "actual position domain")
        if not row['actual']:
            continue
        actual += 1
        t = depth_from_word(L, r, K+32)
        d = digits_from_carries(L, r)
        sum_residue = 9*word_mod(L, r, 7*L-4)
        need(sum_residue == int(row['F_mod_9S']), "exact factor-nine residue")
        need(t == row['t'] and d == int(row['d']), "independent depth and digits")
        need(t <= d+11 <= L-3, "sample target deadline")
        sum_positive += sum_residue == 0
        maximum = max(maximum, t)
    return dict(lengths=len(rows), actual=actual, high_depth_sum_positive=sum_positive,
                maximum_depth=maximum, coverage="all positions at the listed lengths using the proved low-depth bound")


def giant_controls(receipt):
    depths, lengths = [], set()
    for row in receipt['giant_positive_controls']['rows']:
        L, i, S = int(row['L']), int(row['i']), int(row['S'])
        need(L > B and L % 2 == 1 and 3 <= i < L
             and S == 7*L-4 and S % 3 == 0 and S % 5 != 0, "giant domain")
        need(word_mod(L, i, 25*S) == 0, "giant original-word sum")
        t = depth_from_word(L, i, row['K']+32)
        d = digits_from_carries(L, i)
        need(t == row['t'] and d == int(row['d']) and t < row['K'], "giant exact arithmetic")
        need(t <= d+11 and t < L-2, "giant target, nonwitness")
        depths.append(t)
        lengths.add(L)
    return dict(positions=len(depths), distinct_lengths=len(lengths), exact_depths=depths,
                coverage="individual positions only; all low-depth")


def endpoint_controls():
    cutoff, remainder = divmod(700000000000900-1, 1575)
    need(cutoff == 444444444445 and remainder == 24, "strict full-witness cutoff")
    M = (52*10**14+899)//1575
    need(M == 3301587301587 and 52*10**14-(1575*M-900) == 1375,
         "coincident-band lower endpoint coefficient")
    need(52*10**14-(1575*(M+1)-900) == -200, "coincident-band next coefficient")
    for L in (B+1, B+3, M-2, M):
        for i in (3, (L-1)//2, L-1):
            need(digits_from_carries(L, i) == L-14, "band digit endpoint")
    need(digits_from_carries(M+1, M) == M+1-15,
         "lower decimal boundary can change just beyond the band")
    margin = (Fraction(99, 100)-Fraction(58989, 62500))*10**7+12-Fraction(2831472, 25)
    need(margin == Fraction(8712828, 25), "midpoint target bridge margin")
    return dict(full_witness_cutoff=cutoff, coincident_band_end=M,
                midpoint_margin_at_10000000=str(margin))


def main():
    receipt = json.loads((HERE/'verification.json').read_text())
    audited_paths = [HERE/name for name in ('PROOF.md', 'README.md', 'checks.py',
                                           'proof_checks.py', 'verification.json', 'proof-checks.json')]
    audited_paths.append(REPO/'README.md')
    for path in audited_paths:
        at_commit = subprocess.check_output(['git', 'show',
                                             f'{REVIEWED}:{path.relative_to(REPO)}'], cwd=REPO)
        need(at_commit == path.read_bytes(), 'reviewed commit binding: '+str(path))
    report = dict(status="PASS: independent finite review controls",
                  audited_implementation_commit=REVIEWED,
                  source_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
                  input_sha256={str(path.relative_to(REPO)): sha256(path.read_bytes()).hexdigest()
                                for path in audited_paths},
                  signed_carry_controls=carry_controls(),
                  literal_words=literal_controls(),
                  scattered_samples=sample_controls(receipt),
                  giant_positive_controls=giant_controls(receipt),
                  endpoints=endpoint_controls(),
                  scope="Finite review; no global inequality proof or refutation, large enumeration, density investigation, or Lean build.")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
