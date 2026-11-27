#!/usr/bin/env python3
"""Recover all positions from one 3-adic root and logarithm, exactly."""
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = '0a47180b889b392c2323bc1614a473af51f38d78'
FIRST, STEP, COUNT = 31, 6, 256
LAST = FIRST + STEP*(COUNT-1)


def need(ok, message):
    if not ok:
        raise ArithmeticError(message)


def v3(n):
    need(n != 0, 'finite valuation')
    v = 0
    while n % 3 == 0:
        v, n = v+1, n//3
    return v


def root(precision):
    """Newton lift the unique root X^7=10^4 in 1+9Z_3."""
    x, exponent = 1, 2
    need((x**7-10**4) % 9 == 0, 'initial root')
    while exponent < precision:
        exponent = min(2*exponent, precision)
        modulus = 3**exponent
        x = (x - (x**7-10**4)*pow(7*x**6, -1, modulus)) % modulus
        need(pow(x, 7, modulus) == 10**4 % modulus, 'Newton readback')
    need(x % 9 == 1, 'chosen principal root')
    return x


def logarithm(unit, precision):
    """log(unit) modulo 3^precision; no floating point or forbidden division.

    v3(unit-1)>=2. For k>=precision, 2k-v3(k)>=precision,
    so the omitted tail vanishes. Extra v3(k) digits permit exact division.
    """
    z, modulus = unit-1, 3**precision
    need(z % 9 == 0, 'log domain 1+9Z3')
    total = 0
    for k in range(1, precision):
        e = v3(k)
        if 2*k-e >= precision:
            continue
        residue = pow(z, k, modulus*3**e)
        need(residue % 3**e == 0, 'log exact three-power division')
        term = residue//3**e * pow(k//3**e, -1, modulus) % modulus
        total += term if k % 2 else -term
    return total % modulus


def parameters(precision):
    theta = root(precision+2)
    mod = 3**precision
    numerator = (7*theta-25) % (9*mod)
    need(numerator % 9 == 0, 'C numerator precision')
    C = numerator//9 * pow(2, -1, mod) % mod
    lc, lt = logarithm(C, precision), logarithm(10, precision)
    need(v3(C-1) == v3(lc) == 3 and v3(lt) == 2, 'exact log domains')
    d = 3**(precision-2)
    kappa = lc//9 * pow(lt//9, -1, d) % d
    need(kappa % 9 == 6 and pow(10, kappa, mod) == C, 'log quotient readback')
    return theta, C, kappa


def Fmod(L, s, modulus):
    return (7*pow(10, L, modulus)-18*pow(10, s, modulus)-25) % modulus


def member(a, theta, kappa):
    S, d = 3**a, 3**(a-2)
    L, D = (S+4)//7, 2*d
    r = kappa % d
    s = r if r % 2 else r+d
    need(7*L == S+4 and 3 <= s < D and s % 6 == 3 and D > L, 'family class')
    difference = (pow(10, L, 27*S)-theta) % (27*S)
    need(difference != 0 and v3(difference) == a+2, 'exact theta precision')
    need(Fmod(L, s, 9*S) == 0, 'full sum at exact same class')
    i = s if s < L else None
    row = dict(a=a, L=L, S=S, d=d, D=D, class_residue=s, s=s, i=i,
               t=None, first_fail_depth=None, first_fail_n_residue=None)
    if i is None:
        return row
    need(Fmod(L, i, 225*S) == 0, 'all non-seven factors')
    for m in range(1, 65):
        residue = Fmod(L, i, 7**m)
        if residue:
            need(m <= L-2, 'exclusion before full-witness threshold')
            need(Fmod(L, i, 7**(m-1)) == 0, 'exact first failure')
            row.update(t=m-1, first_fail_depth=m,
                       first_fail_n_residue=residue*pow(9, -1, 7**m) % 7**m)
            return row
    raise ArithmeticError('unresolved candidate; resource limit is not exclusion')


def main():
    precision = LAST+1  # extra digit proves v3(10^L-theta)=a+2, even at LAST
    theta, C, kappa = parameters(precision)
    control = member(25, theta, kappa)
    need((control['L'], control['i'], control['t'], control['first_fail_n_residue']) ==
         (121041229921, 40582608819, 2, 294), 'a25 nonzero sum-positive control')
    L, i, S = 313, 51, 2187
    nine = dict(L=L, i=i, S=S, F_mod_S=Fmod(L,i,S),
                F_mod_9S=Fmod(L,i,9*S), n_mod_S=Fmod(L,i,9*S)//9)
    need((nine['F_mod_S'], nine['F_mod_9S'], nine['n_mod_S']) == (0,17496,1944),
         'loss-of-nine control')
    # Compare smaller independently computed precision with truncation.
    for depth in (7, 25, 31, 43, 79):
        small_theta, small_C, small_kappa = parameters(depth)
        need(theta % 3**(depth+2) == small_theta and C % 3**depth == small_C and
             kappa % 3**(depth-2) == small_kappa, 'precision stability')
    cases = [member(FIRST+STEP*u, theta, kappa) for u in range(COUNT)]
    links = []
    for old, new in zip([control]+cases[:-1], cases):
        delta = new['s']-old['s']
        need(delta % old['D'] == 0 and 0 <= delta//old['D'] <= 728, 'all recurrence links')
        links.append(delta//old['D'])
    result = dict(schema=1, base_main=BASE, source_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
                  method='Newton seventh root and modular 3-adic logarithm',
                  specified_exponents=dict(first=FIRST, step=STEP, count=COUNT, last=LAST, next=LAST+STEP),
                  theta_modulus_exponent=precision+2, theta_residue=theta,
                  C_modulus_exponent=precision, C_residue=C,
                  kappa_modulus_exponent=precision-2, kappa_residue=kappa,
                  class_misses=sum(r['i'] is None for r in cases),
                  actual_candidates=sum(r['i'] is not None for r in cases),
                  valuation_histogram=dict(sorted(Counter(str(r['t']) for r in cases if r['i'] is not None).items())),
                  control_a25=control, factor_nine_negative=nine, recurrence_digits=links, cases=cases)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
