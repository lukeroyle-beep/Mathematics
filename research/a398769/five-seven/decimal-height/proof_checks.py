#!/usr/bin/env python3
"""Exact finite controls for the inequalities in PROOF.md; no floats."""
from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


def require(ok, message):
    if not ok:
        raise ValueError(message)


def series(x, terms=80):
    """Log bracket on 1<=x<=2 by the positive atanh series and tail bound."""
    require(1 <= x <= 2, "series range")
    z = (x-1)/(x+1)
    low = 2*sum((z**(2*j+1)/Q(2*j+1) for j in range(terms)), Q(0))
    tail = 2*z**(2*terms+1)/((2*terms+1)*(1-z*z))
    return low, low+tail


def log_interval(x):
    x = Q(x)
    require(x > 0, "positive log input")
    if x < 1:
        low, high = log_interval(1/x)
        return -high, -low
    exponent = 0
    while x >= 2:
        x /= 2
        exponent += 1
    low, high = series(x)
    l2, u2 = series(Q(2))
    return exponent*l2+low, exponent*u2+high


def main():
    l7, u7 = log_interval(7)
    l10, u10 = log_interval(10)
    require(168*u10*u10 < 63*l7**4, "BL coefficient below 63")
    require(10*u7 < Q(39, 2), "degree-one maximum below 19.5")
    # log b' + log log7 + .4 < log(30001.5*log7/log10)+.4.
    _, upper = log_interval(Q(60003, 2)*u7/l10)
    require(upper+Q(2, 5) < Q(53, 5), "normalized maximum below 10.6")
    require(u10 < 3, "integer dynamic log bound")
    require(504*Q(53, 5)**2 == Q(1415736, 25), "strip coefficient")
    slope, constant = Q(58989, 62500), Q(2831472, 25)
    require(Q(1415736, 25)/60000 == slope, "strip slope")
    margin = Q(99, 100)*10**7+12-(slope*10**7+constant)
    require(margin == Q(8712828, 25) and margin > 0
            and slope < Q(99, 100), "exact increasing bridge margin")
    require(157500*11 < 10**10, "q<=floor(L/100) induction base")
    # 10(h+1)>(h+2), for h>=10, propagates the last inequality.
    require(10*(10+1) > 10+2, "q bound recurrence")
    digit_checks = 0
    for L in range(5, 302):
        D = 225*(7*L-4)
        q = len(str(D))
        for i in range(3, L):
            F = 7*10**L-18*10**i-25
            d = len(str(F//D))
            require(d in (L-q+1, L-q+2), "two digit candidates")
            require((d == L-q+2) == (F >= D*10**(L-q+1)),
                    "exact candidate threshold")
            digit_checks += 1
    for L in range(9, 102, 2):
        require(6*7**((L-1)//2-1) > L, "odd half-length period")
        require(225*(7*L-4) < 10**((L+1)//2), "odd half-length size")
    # Failure of the coefficient comparison in PR22 is exact.
    alpha = 1-Q(1, 3*10**16)
    require(alpha > Q(9, 10) and 7**10 < 10**9,
            "PR22 effective exponent insufficient")
    band_end = (52*10**14+899)//1575
    require(band_end == 3301587301587 and band_end % 2 == 1,
            "coincident-deadline band endpoint")
    require(52*10**14-(1575*band_end-900) == 1375
            and (1575*(band_end+1)-900)-52*10**14 == 200,
            "coincident-deadline strict endpoint neighbors")
    print(json.dumps({
        "status": "PASS: finite exact proof controls",
        "source_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "log_method": "80-term positive rational series with geometric tail and powers-of-two reduction",
        "BL_coefficient_less_than": 63,
        "midpoint_maximum_less_than": "53/5",
        "strip_slope": str(slope),
        "strip_constant": str(constant),
        "strip_margin_at_10000000": str(margin),
        "two_digit_candidate_controls": digit_checks,
        "digit_control_lengths_inclusive": [5, 301],
        "digit_control_parity": "both",
        "coincident_deadline_band_inclusive": [1000002000001, band_end],
        "global_inequality": "UNRESOLVED"
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
