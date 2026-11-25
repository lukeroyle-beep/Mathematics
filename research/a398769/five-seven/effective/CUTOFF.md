# What a proved effective estimate would imply

This verifies the conditional cutoff calculation from
[GROWING_POWER.md](../global/GROWING_POWER.md). It does not supply the
missing estimate or change the certified search interval.

Suppose explicit constants `0<=c<1`, `C>=0` and `L0` are proved such that
for every pair in the inherited residual domain with `L>=L0` and the
full digit-sum condition `9*(7L-4)|F`,

```text
v_7(F(L,i)) <= c*L+C*log L.
```

The constants must be uniform in the position and the gap. Put
`delta=1-c>0`. Choose an integer

```text
B >= max(L0, 4, 4/delta, (2*C/delta)^2).
```

An upward integer rounding of any certified upper bound for this maximum
suffices. For computable real parameters, exact equality testing in a
ceiling is unnecessary: use an upper rational enclosure for `C,L0` and
a strictly positive rational lower bound for `delta`, then round upward.

For real `x>=4`, `log x<=sqrt(x)`: the difference is positive at 4
and its derivative `(sqrt(x)-2)/(2x)` is nonnegative. Thus, for integer
`L>B`,

```text
C*log L <= C*sqrt(L) <= delta*L/2,
delta*L/2 > 2,
c*L+C*log L <= L-delta*L/2 < L-2.
```

The first comparison also holds if `C=0`. The strict inequality follows
from `L>B>=4/delta`, not from an unjustified strict rounding at equality.
It contradicts the necessary `v_7(F)>=L-2` of a full witness.

The proved consequence would be absence of full witnesses at `L>B`.
The endpoint `L=B` remains in the finite verification obligation.
If `B<=10,000,000`, the inherited finite certificate would cover every
remaining length. If `B>10,000,000`, all residual odd lengths in
`(10,000,000,B]` would still need exact exhaustive verification or another
proved exclusion, using all allowable positions or the exact two-quotient
procedure. A very large `B` would be an effective reduction with unfinished
finite work, not an all-length exclusion.

No values of the hypothesized triple `(c,C,L0)` have been established
by this investigation. The explicitly chosen parameters in Evertse's
qualitative corollary must not be substituted for them.
