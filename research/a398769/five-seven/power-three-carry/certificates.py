#!/usr/bin/env python3
"""Exact finite certificates, with separate logarithm and decimal-block recovery.

Method A explicitly reuses the inherited Newton/logarithm engine. Method B
uses original decimal blocks and tests all three children of each ternary
digit; it calls no inherited arithmetic. A depth cap raises, never excludes.
All validation uses explicit exceptions and remains enabled under python -O.
"""
import argparse
from collections import Counter
from hashlib import sha256
import importlib.util
import json
from math import gcd
from pathlib import Path
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
FAMILY = HERE.parent
ROOT = HERE.parents[3]
SOURCE = FAMILY / 'power-three' / 'individuals.py'
BASE = '61a6fdfd7f4093b77be36ed0a55fbd3ebf798b7c'
SELECTED = [1231, 1579, 1585, 1591, 1597]


def need(condition, message):
    if not condition:
        raise ArithmeticError(message)


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def Fmod(L, s, modulus):
    return (7*pow(10, L, modulus)-18*pow(10, s, modulus)-25) % modulus


def join(left, right, modulus):
    value, power = left
    other, other_power = right
    return ((value*other_power+other) % modulus, power*other_power % modulus)


def sevens(length, modulus):
    need(length >= 0 and modulus > 0, 'invalid decimal block')
    result, block = (0, 1 % modulus), (7 % modulus, 10 % modulus)
    while length:
        if length % 2:
            result = join(result, block, modulus)
        block = join(block, block, modulus)
        length //= 2
    return result


def decimal_word(L, s, modulus):
    need(0 < s < L, 'decimal word requires an actual position')
    left = join(sevens(L-s-1, modulus), (5 % modulus, 10 % modulus), modulus)
    left = join(left, sevens(s-1, modulus), modulus)
    return join(left, (5 % modulus, 10 % modulus), modulus)[0]


def decimal_representative(a):
    """Recover from n=0 mod S using the original all-sevens block.

    The odd representative is returned whether or not it is an actual
    position. No negative-length word is evaluated when it exceeds L.
    """
    S, L = 3**a, (3**a+4)//7
    target = (sevens(L, S)[0]-2)*pow(2, -1, S) % S
    need(target % 9 == 1, 'decimal target outside principal subgroup')
    position, order, value, shift, modulus = 0, 1, 1, 10, 9
    digits = []
    while modulus < S:
        modulus *= 3
        residues = [(value*pow(shift, child, S)-target) % modulus
                    for child in range(3)]
        children = [child for child, residue in enumerate(residues) if residue == 0]
        need(len(children) == 1, 'ternary child must be unique')
        digit = children[0]
        digits.append(digit)
        position += digit*order
        value = value*pow(shift, digit, S) % S
        order *= 3
        shift = pow(shift, 3, S)
    need(order == 3**(a-2) and pow(10, position, S) == target,
         'decimal ternary recovery readback')
    need(pow(10, order, S) == 1 and pow(10, order//3, S) != 1,
         'exact multiplicative order')
    representative = position if position % 2 else position+order
    need(3 <= representative < 2*order and representative % 6 == 3,
         'least odd representative')
    return representative, dict(a=a, ternary_digits=len(digits),
                                digits_low_first=''.join(map(str, digits)))


def lift(a, sb, depth=8):
    """Predict -4*carry, then test every child by direct exponentiation."""
    D, L = 3**(a-8), (3**a+4)//7
    j, period, divisor = 0, 1, 7
    roots = [dict(depth=1, j=0, period=1)]
    transitions = []
    for m in range(1, depth):
        need(Fmod(L, sb+2*D*j, divisor) == 0, 'current lift must vanish')
        modulus = 7*divisor
        value = Fmod(L, sb+2*D*j, modulus)
        need(value % divisor == 0, 'exact carry division')
        carry = value//divisor
        digit = -4*carry % 7
        residues = [Fmod(L, sb+2*D*(j+c*period), modulus) for c in range(7)]
        need(all(residues[c] == (value+2*c*divisor) % modulus for c in range(7)),
             'coefficient two fails at a child')
        need([c for c in range(7) if residues[c] == 0] == [digit],
             'predicted child differs from direct modular exponentiation')
        transitions.append(dict(m=m, j=j, carry=carry, c=digit,
                                direct_child_F_residues=residues))
        j += digit*period
        period *= 7
        divisor *= 7
        roots.append(dict(depth=m+1, j=j, period=period))
    return dict(roots=roots, transitions=transitions)


def original_certificate(a, s):
    L, S = (3**a+4)//7, 3**a
    need(3 <= s < L, 'certificate requires actual position')
    need(Fmod(L, s, 9*S) == 0, 'same-position nine-times-sum condition')
    nonseven = decimal_word(L, s, 25*S)
    need(nonseven == Fmod(L, s, 225*S)//9 == 0, 'original non-seven factors')
    residues = []
    for m in range(1, 65):
        modulus = 7**m
        residue = decimal_word(L, s, modulus)
        need(9*residue % modulus == Fmod(L, s, modulus), 'word and F disagree')
        residues.append(residue)
        if residue:
            need(m <= L-2, 'nonzero residue exceeds inclusive witness deadline')
            return dict(g=gcd(L, s), q=L//gcd(L, s), n_mod_25S=nonseven,
                        F_mod_9S=0, t=m-1, first_fail_depth=m,
                        first_fail_modulus=modulus, first_nonzero_n_residue=residue,
                        n_residues=residues, full_witness=False)
    raise ArithmeticError('UNRESOLVED at depth cap 64; no exclusion certified')


def literal_controls():
    tested = 0
    for L in range(3, 65):
        for s in range(1, L):
            digits = '7'*(L-s-1)+'5'+'7'*(s-1)+'5'
            n, S, P = int(digits), sum(map(int, digits)), 1
            for digit in digits:
                P *= int(digit)
            F = 7*10**L-18*10**s-25
            need(F == 9*n and S == 7*L-4 and P == 25*7**(L-2),
                 'literal original product, sum, and F')
            need((n % (P*S) == 0) == (F % (225*S*7**(L-2)) == 0),
                 'original full predicate equivalence')
            for modulus in (49, 343, 25*S):
                need(decimal_word(L, s, modulus) == n % modulus, 'literal block control')
            tested += 1
    L, s = 313, 51
    digits = '7'*(L-s-1)+'5'+'7'*(s-1)+'5'
    n, S, P = int(digits), sum(map(int, digits)), 1
    for digit in digits:
        P *= int(digit)
    F = 9*n
    nine = dict(L=L, s=s, S=S, F_mod_S=F % S, F_mod_9S=F % (9*S),
                n_mod_S=n % S, PS_divides_n=n % (P*S) == 0,
                full_F_divides=F % (225*S*7**(L-2)) == 0)
    need((nine['F_mod_S'], nine['F_mod_9S'], nine['n_mod_S']) == (0, 17496, 1944),
         'lost-factor-nine control')
    need(not nine['PS_divides_n'] and not nine['full_F_divides'], 'false literal witness')
    return dict(literal_pairs=tested, lost_factor_nine=nine)


def inherited_audit(kappa):
    """Cross-compare retained independent rows and recheck their arithmetic.

    The old independent reconstruction/search is inherited, not rerun.
    A fresh high-precision kappa and original blocks revalidate every row.
    """
    names = ['power-three/individuals.json', 'power-three/individuals-independent.json',
             'power-three-pair/individual.json', 'power-three-individual/root_log.json',
             'power-three-individual/independent_decimal.json']
    values = [json.loads((FAMILY/name).read_text()) for name in names]
    left, right = values[0]['cases'], values[1]['cases']
    need([r['a'] for r in left] == [r['a'] for r in right] == list(range(31, 1562, 6)),
         'complete 256-row inherited domain')
    fields = ['a', 'L', 's', 'i', 't', 'first_fail_depth', 'first_fail_n_residue']
    for x, y in zip(left, right):
        need(all(x[f] == y[f] for f in fields), 'inherited independent rows disagree')
    p = {r['a']: r for r in values[3]['cases']}
    d = {r['a']: r for r in values[4]['rows']}
    for a in [1567, 1573, 1579]:
        need(all(p[a][f] == d[a][f] for f in fields), 'late inherited rows disagree')
    pair = values[2]['new_a1567']
    need(all(pair[f] == p[1567][f] for f in ['L', 's', 'i', 't', 'first_fail_n_residue']),
         'inherited pair certificate disagreement')
    rows = left+[p[a] for a in [1567, 1573, 1579]]
    need([r['a'] for r in rows] == list(range(31, 1580, 6)), 'complete 259-member domain')
    checked = []
    for r in rows:
        a, L, s = r['a'], r['L'], r['s']
        S, d = 3**a, 3**(a-2)
        residue = kappa % d
        actual_s = residue if residue % 2 else residue+d
        need(L == (S+4)//7 and s == actual_s and Fmod(L, s, 9*S) == 0,
             'fresh inherited kappa, length, or sum readback')
        actual = 3 <= s < L
        need(actual == (r['i'] is not None), 'inherited actual classification')
        row = dict(a=a, actual=actual, t=r['t'])
        if actual:
            fresh = original_certificate(a, s)
            need((fresh['t'], fresh['first_fail_depth'], fresh['first_nonzero_n_residue']) ==
                 (r['t'], r['first_fail_depth'], r['first_fail_n_residue']),
                 'fresh inherited original-word exclusion disagrees')
            row.update(first_fail_depth=fresh['first_fail_depth'],
                       first_nonzero_n_residue=fresh['first_nonzero_n_residue'])
        else:
            need(s >= L and r['t'] is None, 'class miss not established')
        checked.append(row)
    return dict(count=259, first=31, last=1579, next=1585,
                original_independent_reconstruction='inherited; not rerun for all 259 rows',
                fresh_checks='high-precision kappa; exact length and range; original decimal blocks and all failure residues',
                input_sha256={name:digest(FAMILY/name) for name in names}, rows=checked)


def audit():
    spec = importlib.util.spec_from_file_location('inherited_newton_log', SOURCE)
    engine = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(engine)
    precision = 1598
    theta, C, kappa = engine.parameters(precision)
    # A separate modular-inverse-exponent construction checks the root itself.
    theta_direct = pow(10, 4*pow(7, -1, 3**precision), 3**(precision+2))
    need(theta == theta_direct, 'Newton versus direct root construction')
    need(pow(10, kappa, 3**precision) == C, 'global logarithm readback')
    required = sorted(set([25, 31]+SELECTED+[a-6 for a in SELECTED]))
    recovered, traces = {}, []
    for a in required:
        d = 3**(a-2)
        r = kappa % d
        first = r if r % 2 else r+d
        second, trace = decimal_representative(a)
        need(first == second, 'independent representative disagreement at '+str(a))
        recovered[a] = first
        traces.append(trace)
    rows = []
    for a in SELECTED:
        b, D = a-6, 3**(a-8)
        L, sb, sa = (3**a+4)//7, recovered[a-6], recovered[a]
        need((sa-sb) % (2*D) == 0, 'increment not integral')
        k, K = (sa-sb)//(2*D), (L-1-sb)//(2*D)
        need(0 <= k <= 728 and K <= 468, 'increment endpoints')
        actual = 3 <= sa < L
        need(actual == (k <= K), 'actuality/increment equivalence')
        lifts = lift(a, sb)
        j5 = lifts['roots'][4]['j']
        row = dict(a=a, b=b, L=L, D=D, s_b=sb, s_a=sa, k=k, K=K,
                   previous_length=(3**b+4)//7, previous_representative_actual=sb<(3**b+4)//7,
                   j_5=j5, actual=actual, lifts=lifts,
                   depth_five_outcome=('range_miss' if j5>K else
                                       'actual_increment_miss' if j5!=k else 'actual_survivor'))
        if actual:
            row.update(original_certificate(a, sa))
        rows.append(row)
    # Pilot expectations enter only after every independent reconstruction.
    pilots = {1585:(450,922,1,28,49), 1591:(191,780,1,42,49),
              1597:(92,2255,2,294,343), 1579:(205,119,1,14,49),
              1231:(377,720,4,14406,16807)}
    for r in rows:
        need((r['k'],r['j_5'],r['t'],r['first_nonzero_n_residue'],
              r['first_fail_modulus']) == pilots[r['a']],
             'pilot comparison after reconstruction at '+str(r['a'])+': '+
             str((r['k'],r['K'],r['j_5'],r['t'],r['first_nonzero_n_residue'],r['first_fail_modulus'])))
        if r['a'] >= 1585:
            need(r['K'] == 468, 'new-member K pilot after reconstruction')
    deep = next(r for r in rows if r['a'] == 1231)
    need(all((deep['k']-r['j']) % r['period'] == 0 for r in deep['lifts']['roots'][:4])
         and deep['j_5']>deep['K'], 'actual depth-four survivor failure mode')
    inside = next(r for r in rows if r['a'] == 1579)
    need(inside['j_5'] <= inside['K'] and inside['j_5'] != inside['k'],
         'in-range root but wrong actual increment control')
    positive = dict(a=25, L=(3**25+4)//7, s=recovered[25],
                    **original_certificate(25, recovered[25]))
    need(positive['n_mod_25S'] == 0 and positive['n_residues'] == [0,0,294],
         'nonzero positive full-sum control')
    base = dict(a=31, L=(3**31+4)//7, s=recovered[31],
                **original_certificate(31, recovered[31]))
    need(base['n_residues'] == [0,35], 'inherited base case')
    inherited = inherited_audit(kappa)
    all_rows = inherited['rows']+[r for r in rows if r['a']>=1585]
    need([r['a'] for r in all_rows] == list(range(31,1598,6)), '262-member coverage')
    histogram = dict(sorted(Counter(str(r['t']) for r in all_rows if r['actual']).items()))
    return dict(schema=1, base_main=BASE, status='PASS', source_sha256=digest(Path(__file__)),
                method_A='explicit reuse of inherited Newton seventh root and 3-adic logarithm',
                method_B='independent original decimal-block target and exhaustive three-child ternary lifting',
                inherited_source_path=str(SOURCE.relative_to(ROOT)), inherited_source_sha256=digest(SOURCE),
                precision=precision, root_crosscheck='direct modular-inverse exponent agrees',
                ternary_recovery_exponents=required, ternary_traces=traces, rows=rows,
                positive_a25=positive, inherited_base_a31=base, controls=literal_controls(),
                inherited_259=inherited, named_family_members_excluded=262,
                last_family_exponent=1597, next_family_exponent=1603,
                class_misses=sum(not r['actual'] for r in all_rows),
                actual_candidates=sum(r['actual'] for r in all_rows), valuation_histogram=histogram,
                new_exclusions=[1585,1591,1597], no_depth_cap_exclusions=True,
                whole_length_endpoint_inclusive=1000002000000, moving_family='OPEN',
                unrestricted_five_seven='OPEN', wider_digit_one='OPEN', Lean_verification=False)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', type=Path)
    args = parser.parse_args()
    result = json.dumps(audit(), indent=2, sort_keys=True)+'\n'
    if args.check:
        need(args.check.read_text() == result, 'retained receipt differs from fresh computation')
    print(result, end='')


if __name__ == '__main__':
    main()
