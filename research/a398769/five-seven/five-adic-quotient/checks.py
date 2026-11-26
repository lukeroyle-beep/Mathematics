#!/usr/bin/env python3
"""Exact rational constants and literal-word checks; no external dependencies."""
from fractions import Fraction as Q
from hashlib import sha256
from math import prod
import json

B = 1_000_002_000_000
N = 10**12


def require(condition, message):
    if not condition:
        raise ArithmeticError(message)


def log_bounds(x, terms=100):
    """atanh series after power-of-two reduction, with an explicit tail."""
    x = Q(x)
    require(x > 0, 'positive logarithm argument')
    k = 0
    while x >= 2:
        x /= 2
        k += 1
    while x < 1:
        x *= 2
        k -= 1

    def core(y):
        z = (y - 1) / (y + 1)
        lo = 2 * sum((z**(2*j+1) / (2*j+1) for j in range(terms)), Q(0))
        tail = 2*z**(2*terms+1) / ((2*terms+1)*(1-z*z))
        return lo, lo + tail

    a, b = core(x)
    c, d = core(Q(2))
    return (a+k*c, b+k*d) if k >= 0 else (a+k*d, b+k*c)


def enclosed(x, lower, upper):
    lo, hi = log_bounds(x)
    require(Q(lower) < lo and hi < Q(upper), f'log enclosure {x}')


def constants():
    enclosed(2, Q(69,100), Q(7,10))
    enclosed(3, 1, Q(11,10))
    enclosed(5, Q(8,5), 2)
    enclosed(7, Q(389,200), Q(39,20))
    enclosed(10, Q(23,10), Q(2303,1000))
    enclosed(63, 4, Q(21,5))
    coefficient = 120*Q(2)/Q(8,5)**4
    require(coefficient == Q(9375,256) and coefficient < 48, 'coefficient')
    require(2*10**9+1 < 3*10**9, 'b-prime relaxation')
    first_max = Q(11,10)+9*Q(2303,1000)+Q(7,10)+Q(2,5)
    require(first_max == Q(22927,1000) and first_max < 24, 'first maximum')
    require(10*Q(2) < 24 and 10 < 24, 'other maximum branches')
    gap = Q(1,25000)-Q(48*24**2,10**9)
    require(gap == Q(193,15625000) and gap*N > 2, 'strict contradiction')
    poly_margin = Q(N,10**9)-Q(21,5)-36*12*Q(2303,1000)
    require(poly_margin == Q(113,125) and poly_margin > 0, 'polynomial base')
    derivative = Q(1,10**9)-Q(36,N)
    require(derivative > 0, 'polynomial persistence')
    # Independent replay of the inherited units-end affine comparison.
    require(168*Q(2303,1000)**2/Q(389,200)**4 < 63, 'inherited coefficient')
    edge_first = log_bounds(Q(25001)/Q(23,10))[1]+Q(7,10)+Q(2,5)
    require(edge_first < 11, 'inherited first max branch')
    edge_margin = 10**7-2-(1+Q(95823,4)*(Q(10**7,25000)+1))
    require(edge_margin == Q(1574965,4) and Q(95823,100000)<1, 'inherited edge margin')
    # Exact enclosures for the residual gap; decimals here are rationals.
    l10, u10 = log_bounds(10)
    l7, u7 = log_bounds(7)
    slope_lo, slope_hi = l10-u7-Q(1,10**9), u10-l7-Q(1,10**9)
    require(Q('0.3566749429') < slope_lo < slope_hi < Q('0.3566749430'), 'gap slope')
    lconst, uconst = log_bounds(Q(343,25))
    width_lo, width_hi = lconst+slope_lo*(B+1), uconst+slope_hi*(B+1)
    require(356675656291 < width_lo < width_hi < 356675656292, 'gap at B+1')
    tslope_lo, tslope_hi = (l10-Q(1,10**9))/u7, (u10-Q(1,10**9))/l7
    require(Q('1.1832946619') < tslope_lo < tslope_hi < Q('1.1832946620'), 't upper slope')
    require(6*7**13 <= B+1 < 6*7**14, 'first K equals 15')
    require(Q(225,89) > Q(252,100) and Q(225,89)<Q(253,100), '37/89 radius')
    return {
        'log_method': '100-term atanh series after binary reduction with positive tail bound',
        'coefficient_rational_upper': str(coefficient),
        'maximum_first_rational_upper': str(first_max),
        'contradiction_slope_gap': str(gap),
        'contradiction_margin_at_10pow12': str(gap*N-2),
        'polynomial_base_margin': str(poly_margin),
        'polynomial_derivative_lower': str(derivative),
        'inherited_edge_margin_at_10pow7': str(edge_margin),
        'gap_slope_open_enclosure': ['0.3566749429','0.3566749430'],
        'gap_at_B_plus_1_open_enclosure': [356675656291,356675656292],
        't_upper_slope_open_enclosure': ['1.1832946619','1.1832946620'],
        'K_at_B_plus_1': 15,
    }


def valuation(n, p):
    require(n != 0, 'finite valuation')
    e = 0
    while n % p == 0:
        n //= p
        e += 1
    return e


def literal_words():
    counts = dict(words=0, three_divides_S=0, sum_passes=0,
                  sum_passes_three_divides_S=0, five_free_sum_passes=0,
                  seven_positive=0, full_witnesses=0, factor_nine_negatives=0)
    digest = sha256()
    examples = {}
    for L in range(5,252,2):
        for i in range(3,L):
            word = ['7']*L
            word[L-1] = word[L-1-i] = '5'
            text = ''.join(word)
            n = int(text)
            S, P = sum(map(int,text)), prod(map(int,text))
            F = 7*10**L-18*10**i-25
            require(S == 7*L-4 and P == 25*7**(L-2) and 9*n == F, 'literal identity')
            t = valuation(F,7)
            C = F//(25*7**t)
            require(F == 25*C*7**t and C%5 and C%7 and C%9==0, 'seven-free cofactor')
            require(valuation(F,5)==2 and valuation(C*7**t+1,5)==i-2, 'five-adic valuation')
            require(25*(C*7**t+1)==10**i*(7*10**(L-i)-18), 'digit identity')
            require(0 < F//25 < 7**(2*L) and t<2*L, 't upper bound')
            sum_pass = n%S == 0
            require(sum_pass == (F%(9*S)==0), 'factor nine exactness')
            full = n%(P*S)==0
            require(full == (F%(225*S*7**(L-2))==0), 'full divisor')
            require(full == (S%5!=0 and sum_pass and t>=L-2), 'full equivalence')
            require((S%5!=0 and sum_pass) == (C%(9*S)==0), 'cofactor divisibility')
            if full:
                q = n//(P*S)
                q0 = q//7**valuation(q,7)
                require(C==9*S*q0 and t==L-2+valuation(q,7), 'exact quotient')
            row={'L':L,'i':i,'t':t,'S':S}
            counts['words'] += 1
            counts['three_divides_S'] += S%3==0
            counts['sum_passes'] += sum_pass
            counts['sum_passes_three_divides_S'] += sum_pass and S%3==0
            counts['five_free_sum_passes'] += sum_pass and S%5!=0
            counts['seven_positive'] += t>0
            counts['full_witnesses'] += full
            bad=F%S==0 and not sum_pass
            counts['factor_nine_negatives'] += bad
            for name, ok in [('sum_pass',sum_pass and S%5!=0),
                             ('sum_pass_three',sum_pass and S%3==0 and S%5!=0),
                             ('factor_nine_negative',bad),('depth_positive',t>=2)]:
                if ok and name not in examples:
                    examples[name]=row
            digest.update(f'{L},{i},{t},{int(sum_pass)},{int(full)}\n'.encode())
    for name in ['sum_passes_three_divides_S','five_free_sum_passes','seven_positive','factor_nine_negatives']:
        require(counts[name]>0, f'nonzero control {name}')
    require(counts['full_witnesses']==0, 'bounded literal scan has no witness')
    return {'odd_lengths_inclusive':[5,251], 'positions':'every 3 <= i < L',
            'counts':counts,'examples':examples,'stream_sha256':digest.hexdigest(),
            'scope':'identity and predicate controls; no new consecutive endpoint credit'}


def main():
    print(json.dumps({'status':'PASS','constants':constants(),'literal_words':literal_words()},indent=2,sort_keys=True))


if __name__ == '__main__':
    main()
