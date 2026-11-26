#!/usr/bin/env python3
"""Direct full-period audit of bounded successive transition congruences.

Every start in each complete period is visited. The depth-three prefilter
is itself a complete enumeration of all 729 increments; each retained
increment is checked in the requested full modulus. No survivor set from
one reported depth is used to select starts at a later depth.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = HERE.parent


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def pair(u: int, m: int) -> tuple[int, int]:
    """Reduce exponents first; exact division keeps the length residue."""
    q = 7**m
    order = 6 * 7**(m - 1)
    a = 31 + 6*u
    three = pow(3, a, 7*order)
    require((three + 4) % 7 == 0, 'nonintegral length residue')
    length = (three + 4)//7
    d2 = 2*pow(3, a - 2, order) % order
    return (7*pow(10, length, q) - 25) % q, pow(10, d2, q)


def all_increments(u: int, m: int) -> list[int]:
    """Unfiltered enumeration used for low-depth and nonzero controls."""
    mod = 7**m
    lhs, g = pair(u, m)
    rhs, _ = pair(u + 1, m)
    result = []
    for k in range(729):
        if lhs == rhs:
            result.append(k)
        lhs = lhs*g % mod
    return result


def low_depth_candidates() -> list[list[int]]:
    result = [all_increments(u, 3) for u in range(7)]
    for u, ks in enumerate(result):
        require(bool(ks), f'vacuous depth-three prefilter at {u}')
        require(all(k % 7 == 0 and k % 49 != 0 for k in ks),
                'depth-three increments disagree with exact v7(k)=1')
        require(all(b-a == 49 for a, b in zip(ks, ks[1:])),
                'depth-three candidates not the complete progression')
        require(all_increments(u+7, 3) == ks, 'low-depth period fails')
    return result


def full_period(m: int, low: list[list[int]]) -> dict:
    mod = 7**m
    order = 6*7**(m-1)
    period = 7**(m-2)
    length = ((3**31+4)//7) % order
    d2 = 2*3**29 % order
    current_u = (7*pow(10, length, mod)-25) % mod
    previous: list[int] = []
    first: list[int] = []
    starts = []
    edge_count = 0
    increment_count = 0
    # Hash every edge, including each empty one: fixes ordering and full scope.
    edges_hash = hashlib.sha256()
    for u in range(period):
        next_length = (729*length - 416) % order
        next_u = (7*pow(10, next_length, mod)-25) % mod
        g = pow(10, d2, mod)
        candidates = low[u % 7]
        lhs = current_u*pow(g, candidates[0], mod) % mod
        step = pow(g, 49, mod)
        ks = []
        for k in candidates:
            if lhs == next_u:
                ks.append(k)
            lhs = lhs*step % mod
        # Since m>=5, order(G)=7^(m-1)>728: at most one increment.
        require(len(ks) <= 1, 'unexpected duplicate bounded increment')
        if ks:
            edge_count += 1
            increment_count += len(ks)
            require(current_u*pow(g, ks[0], mod) % mod == next_u,
                    'transition residue check failed')
        edges_hash.update((str(u)+':'+','.join(map(str, ks))+'\n').encode())
        if u == 0:
            first = ks
        elif previous and ks:
            starts.append({'u': u-1, 'first_increments': previous,
                           'second_increments': ks})
        previous = ks
        length = next_length
        d2 = 729*d2 % order
        current_u = next_u
    if previous and first:
        starts.append({'u': period-1, 'first_increments': previous,
                       'second_increments': first})
    require(pair(period, m) == pair(0, m), 'period endpoint check failed')
    for row in starts:
        u = row['u']
        require(all_increments(u, m) == row['first_increments'],
                'first increment independent direct recheck failed')
        require(all_increments(u+1, m) == row['second_increments'],
                'second increment independent direct recheck failed')
    # Complete brute force over all u and all k at the first reported depth.
    if m == 5:
        raw_edges = [all_increments(u, m) for u in range(period)]
        raw_starts = [
            {'u': u, 'first_increments': raw_edges[u],
             'second_increments': raw_edges[(u+1) % period]}
            for u in range(period)
            if raw_edges[u] and raw_edges[(u+1) % period]
        ]
        require(raw_starts == starts, 'unfiltered depth-five control failed')
        raw_hash = hashlib.sha256()
        for u, ks in enumerate(raw_edges):
            raw_hash.update((str(u)+':'+','.join(map(str, ks))+'\n').encode())
        require(raw_hash.digest() == edges_hash.digest(),
                'all depth-five edges disagree with unfiltered enumeration')
    return {'m': m, 'period': period, 'visited_starts': period,
            'edge_count': edge_count, 'increment_count': increment_count,
            'two_transition_start_count': len(starts),
            'all_edges_sha256': edges_hash.hexdigest(), 'starts': starts}


def main() -> None:
    low = low_depth_candidates()
    levels = [full_period(m, low) for m in range(5, 10)]
    control_u = 14984
    mod = 7**8
    u0, g0 = pair(control_u, 8)
    u1, g1 = pair(control_u+1, 8)
    u2, _ = pair(control_u+2, 8)
    require(u0*pow(g0, 189, mod) % mod == u1, 'first positive control fails')
    require(u1*pow(g1, 42, mod) % mod == u2, 'second positive control fails')
    require(all_increments(control_u, 8) == [189], 'control increment not unique')
    require(all_increments(control_u+1, 8) == [42], 'control increment not unique')
    control = {'m': 8, 'u': control_u, 'first_increment': 189,
               'second_increment': 42, 'U': [u0, u1, u2], 'G': [g0, g1],
               'first_residual': (u0*pow(g0,189,mod)-u1)%mod,
               'second_residual': (u1*pow(g1,42,mod)-u2)%mod}
    sources = [
        'sum-position-escape/README.md', 'sum-position-escape/MATH_REVIEW.md',
        'fixed-depth/PROOF.md', 'effective/QUALITATIVE.md',
    ]
    output = {
        'schema': 1,
        'method': 'direct enumeration of every u in each full period; complete depth-three increment prefilter',
        'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'inherited_inputs_sha256': {p: hashlib.sha256((BASE/p).read_bytes()).hexdigest() for p in sources},
        'increment_domain': [0,728], 'low_depth_prefilter': low,
        'wraparound_included': True, 'levels': levels,
        'depth_nine_has_no_projected_starts': levels[-1]['two_transition_start_count'] == 0,
        'positive_control': control,
        'scope': 'projected necessary transitions; no actual sum-position or single-member exclusion inferred',
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
