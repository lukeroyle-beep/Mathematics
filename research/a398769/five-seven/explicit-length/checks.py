#!/usr/bin/env python3
"""Exact constants and endpoint controls; no project imports or floating point."""
import json
from fractions import Fraction as Q
from math import factorial, gcd


def require(ok, message):
    if not ok:
        raise ArithmeticError(message)


def log_interval(x, terms=40):
    z = (x - 1) / (x + 1)
    require(0 <= z < 1, 'log domain')
    lo = 2 * sum((z**(2*j+1) / (2*j+1) for j in range(terms)), Q(0))
    hi = lo + 2*z**(2*terms+1)/((2*terms+1)*(1-z*z))
    return lo, hi


def valuation(n, p):
    require(n > 0, 'positive valuation argument')
    t = 0
    while n % p == 0:
        n //= p
        t += 1
    return t


def K_of(L):
    k, period = 1, 6
    while period <= L:
        k, period = k+1, 7*period
    return k


def r_bound(k):
    return 1+252*(k+1)**2*((k+1)+272*k**4+64*k**3)


def square_bound(k):
    return 1+252*(k+1)**2*((k+1)+k**8+2*k**6)


def main():
    B = 1000002000000
    lo2, hi2 = log_interval(Q(2))
    lo7r, hi7r = log_interval(Q(7, 4))
    lo10r, hi10r = log_interval(Q(5, 4))
    lo7, hi7 = lo7r+2*lo2, hi7r+2*hi2
    lo10, hi10 = lo10r+3*lo2, hi10r+3*hi2
    require(168*hi10**2 < 63*lo7**4, 'C0 < 63')
    require(Q(3, 2) < lo7 < hi7 < 2 < lo10 < hi10 < Q(5, 2), 'log bounds')
    require(Q(1, 2) < lo2 < hi2 < 1, 'log two')
    # Elementary source constants and conservative logarithmic cutoffs.
    require(sum(Q(5, 2)**j/factorial(j) for j in range(8)) > 10, 'exp(5/2)>10')
    require((8*30**6)**2*3**9 < 10**24, 'real logarithm coefficient')
    require(48**6*3*4*8 < 2*10**12, 'p-adic coefficient')
    require(12*10**12*43 < 10**16 and 8*10**12*101 < 10**16, 'signed cutoffs')
    require(57*10**16 < 10**18 and 7**10 < 10**9, 'quotient bound and insufficient exponent')

    U_moving = r_bound(15)+2
    U_square = square_bound(19)+2
    require(U_moving == 902265864195 < B, 'moving cutoff')
    require(6*7**13 < U_moving, 'K<=14 branch')
    require(r_bound(16)+1 < 6*7**14, 'moving induction base')
    require(17**6 < 2*16**6 < 7*16**6, 'degree six growth')
    require(U_square == 1721427606158403, 'square cutoff')
    require(6*7**17 < U_square, 'K<=18 branch')
    require(square_bound(20)+1 < 6*7**18, 'square induction base')
    require(6**10 < 7*5**10, 'degree ten growth')
    # Finite controls for the symbolic monotonicity substitutions, not their proof.
    centre_checks = 0
    for k in range(9, 101):
        for b in range(2, k*k+1):
            H = Q(k*k, b)+b+1
            require(b**3*H <= k**8+2*k**6, 'square coefficient substitution')
            if b <= 4*k:
                require(b**3*H <= 272*k**4+64*k**3, 'moving coefficient substitution')
            centre_checks += 1
    for k in range(16, 201):
        require(r_bound(k)+1 < 6*7**(k-2), 'moving induction controls')
    for k in range(20, 201):
        require(square_bound(k)+1 < 6*7**(k-2), 'square induction controls')

    conditional = 444444444445
    require(1575*conditional < 700000000000900 <= 1575*(conditional+1), 'strict decimal cutoff')
    band_end = 3301587301587
    require(52*10**14-(1575*band_end-900) == 1375, 'band last integer')
    require(52*10**14-(1575*(band_end+1)-900) == -200, 'band successor')

    # Literal arithmetic independently checks lift indexing on affordable inputs.
    literal_pairs, actual_lifts, sum_passes = 0, 0, 0
    for L in range(5, 202, 2):
        K = K_of(L)
        require(6*7**(K-1) > L and (K == 1 or 6*7**(K-2) <= L), 'least K')
        require(K <= L-2, 'witness depth covers K')
        high = []
        for i in range(3, L):
            word = '7'*(L-i-1)+'5'+'7'*(i-1)+'5'
            n = int(word)
            S = sum(map(int, word))
            F = 9*n
            t = valuation(F, 7)
            require(F == 7*10**L-18*10**i-25, 'literal F identity')
            require(5*10**L < F < 7*10**L, 'size bounds')
            if t >= K:
                high.append(i)
                for j in range(K, t+1):
                    digit = (5*(F//7**j)) % 7
                    children = [i+a*6*7**(j-1) for a in range(7)]
                    hits = [x for x in children if (7*pow(10, L, 7**(j+1))-18*pow(10, x, 7**(j+1))-25) % 7**(j+1) == 0]
                    require(hits == [children[digit]], 'unique lift by seven-child control')
                    require((digit == 0) == (j < t), 'first nonzero at t')
                actual_lifts += 1
            if S % 5 and n % S == 0:
                H = F//(225*S)
                require(F % (225*S) == 0 and H > 0 and valuation(H, 7) == t, 'sum cofactor exact')
                digits = len(str(H))
                require((10**t <= 10**12*H) == (t <= digits+11), 'decimal equivalence')
                sum_passes += 1
            literal_pairs += 1
        require(len(high) <= 1, 'at most one actual depth K position')
    require(sum_passes > 0 and actual_lifts > 0, 'nonvacuous controls')

    # Check the calibration with arbitrary exact rational delta and C.
    calibration_checks = 0
    for delta in (Q(1, 2), Q(1, 7), Q(2, 3)):
        for C in (Q(-3, 2), Q(0), Q(17, 3)):
            for L0 in (5, 17):
                cutoff = max(L0-1, (C+2)//delta)
                for L in range(5, 101):
                    if L >= L0 and L-2 <= (1-delta)*L+C:
                        require(L <= cutoff, 'calibration upper bound')
                    calibration_checks += 1
    print(json.dumps({'status':'PASS', 'B':B, 'global_U':None,
        'moving_centre':{'U':U_moving,'R15':r_bound(15),'R16':r_bound(16),'T15':6*7**14,'closed_by_inherited_B':True},
        'square_centre':{'U':U_square,'R19':square_bound(19),'R20':square_bound(20),'T19':6*7**18,'remaining_odd_L':[B+1,U_square]},
        'seven_free_quotient':{'U0':10**18-1,'U100':10**18*101**2-1},
        'decimal_height':{'conditional_U':conditional,'equivalent_band_end':band_end,'proved_global':False},
        'C0_less_than_63':True,'coefficient_controls':centre_checks,
        'literal_pairs':literal_pairs,'actual_high_depth_positions':actual_lifts,'sum_positive_pairs':sum_passes,
        'calibration_controls':calibration_checks,'new_whole_lengths':0},indent=2,sort_keys=True))


if __name__ == '__main__':
    main()
