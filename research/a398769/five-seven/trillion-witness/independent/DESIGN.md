# Independent original-digit verification design

This design was fixed before reading any new discovery output. Inputs are only
integers `(L,i)` and the original decimal block description, from most to least
significant: `7^(L-i-1) 5 7^(i-1) 5`, where exponents mean repetition counts.
No discovery module, discrete logarithm, lift digit, or supplied residue is
imported. The implementation reconstructs length, digit sum, symbolic digit
product, and positions of the fives from these runs.

For each modulus `m`, a block is represented by `(p,v)`, with `p=10^length mod m`
and `v` the integer value of its decimal digits modulo `m`. Concatenation is
`(p,v)*(q,w)=(pq,vq+w) mod m`. Repeated squaring of the one-digit block computes
a repeated digit run in logarithmically many operations. This is an associative
operation by direct expansion, has identity `(1,0)`, and is exactly decimal
concatenation. Thus the four-block residue equals the original integer's residue
without dividing by nine or using the search formula for its numerator.

Tests start with `n mod S`, `n mod 125`, then `n mod 7^d` at doubling depths.
A nonzero last residue has exactly the same seven-adic valuation as `n` provided
that valuation is smaller than `d`; repeated exact division of this residue
therefore certifies the first failed power. Zero through a bounded depth certifies
only that depth. A witness verdict additionally requires `5` not dividing `S`,
`n mod S=0`, `n mod 25=0`, and zero through the entire exponent `L-2`.
No depth cap is silently promoted to a full divisibility certificate.

For the factor-nine obligation, direct `n mod S` is used even when `3|S`.
It is equivalent to the search's `9S|9n` and cannot accidentally test only
`S|9n`. The verifier retains `9*(n mod S)` as an independently derived residue
of `9n` modulo `9S`, solely for comparing discovery certificates.

Self-controls compare original constructed decimal integers against the monoid
for every legal position at odd lengths 5 through 65 and multiple moduli,
including non-coprime moduli, plus a targeted `(313,51)` factor-nine trap. Positive digit-sum controls and a case where
`S|9n` but `S` does not divide `n` guard the factor-nine distinction. Assertions
are not used as correctness guards, so optimized Python has the same behavior.
