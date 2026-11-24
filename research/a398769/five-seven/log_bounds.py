#!/usr/bin/env python3
"""Rigorous natural logarithm intervals using rational arithmetic only."""
from fractions import Fraction as Q


def log_interval(x, n=20):
    """Bounds for log(x), x>=1; sum n terms and bound the positive tail."""
    z = (x - 1) / (x + 1)
    assert 0 <= z < 1
    lower = 2 * sum((z**(2*k+1) / (2*k+1) for k in range(n)), Q(0))
    upper = lower + 2*z**(2*n+1) / ((2*n+1)*(1-z*z))
    return lower, upper


def reduced_log_interval(x, twos):
    lower, upper = log_interval(x)
    lo2, hi2 = log_interval(Q(2))
    return lower + twos*lo2, upper + twos*hi2


if __name__ == '__main__':
    lo7, hi7 = reduced_log_interval(Q(7, 4), 2)
    lo10, hi10 = reduced_log_interval(Q(5, 4), 3)
    lo2575, hi2575 = reduced_log_interval(Q(2575, 2048), 11)
    assert Q('1.9459') < Q('1.94591014') < lo7 < hi7 < Q('1.94591015') < Q('1.946')
    assert Q('2.30258509') < lo10 < hi10 < Q('2.30258510') < Q('2.3026')
    assert Q('7.85360481') < lo2575 < hi2575 < Q('7.85360482') < Q('7.8537')
    coarse = 168*Q('2.3026')*Q('7.8537') / Q('1.9459')**4
    assert 168*hi10*hi2575 / lo7**4 < coarse < 212
    print('PASS: exact rational log intervals and prefactor < 212')
