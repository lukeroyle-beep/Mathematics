#!/usr/bin/env python3
"""Literal-decimal controls for independent.cpp, with checks active under -O."""
import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
import subprocess
import tempfile


def require(value, message):
    if not value:
        raise RuntimeError(message)


def run(binary, scratch, k, b, low, high, depth, radius):
    pair_path, deep_path, receipt_path = [scratch / name for name in ('pairs.csv', 'deep.csv', 'receipt.json')]
    subprocess.run([str(binary), '--K', str(k), '--b', str(b), '--lo', str(low), '--hi', str(high), '--depth', str(depth), '--h-limit', str(radius), '--pairs', str(pair_path), '--pairs22', str(deep_path), '--json', str(receipt_path)], check=True)
    pairs = [tuple(map(int, row)) for row in csv.reader(pair_path.open())]
    return pairs, json.loads(receipt_path.read_text())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--binary', required=True, type=Path)
    args = parser.parse_args()
    binary = args.binary.resolve()
    checks, all_pairs, positive_sum, singular_positive, lost_nine_negative = 0, 0, 0, 0, 0
    offsets = set()
    digest = hashlib.sha256()
    with tempfile.TemporaryDirectory() as temp:
        scratch = Path(temp)
        for b in range(2, 17):
            for depth in (1, 2, 3, 4):
                expected, free, sum_pass = [], 0, 0
                for length in range(3, 502, 2):
                    for i in range(3, length, 6):
                        word = '7' * (length - i - 1) + '5' + '7' * (i - 1) + '5'
                        n = int(word)
                        S = sum(map(int, word))
                        require(S == 7 * length - 4, 'literal sum')
                        require(9*n == 7*10**length - 18*10**i - 25, 'literal F')
                        if (9*n) % (7**depth):
                            continue
                        for a in range(1, b):
                            if math.gcd(a, b) != 1:
                                continue
                            h = b*i - a*length
                            if abs(h) <= 16:
                                expected.append((a, h, length, i))
                                offsets.add(h)
                                lost_nine_negative += (9*n) % S == 0 and n % S != 0
                                if S % 5:
                                    free += 1
                                    sum_pass += n % S == 0
                                singular_positive += a % 7 == 0 and depth >= 2
                expected.sort()
                pairs, receipt = run(binary, scratch, 4, b, 3, 501, depth, 16)
                require(pairs == expected, f'direct coverage b={b}, depth={depth}')
                require(receipt['pairs13'] == len(expected), 'pair count')
                require(receipt['fivefree13'] == free, 'fivefree count')
                require(receipt['sum13'] == sum_pass, 'literal digit sum count')
                require(receipt['pairs22'] == 0, 'small exact depth22 control')
                require(receipt['raw_lines'] == sum(math.gcd(a,b)==1 for a in range(1,b))*33, 'raw count')
                compatible = sum((h-3*b+a)%(2*math.gcd(3,a)) == 0 for a in range(1,b) if math.gcd(a,b)==1 for h in range(-16,17))
                require(receipt['compatible_lines'] == compatible, 'independent compatibility count')
                for row in pairs:
                    digest.update((','.join(map(str,row))+'\n').encode())
                checks += 1
                all_pairs += len(pairs)
                positive_sum += sum_pass
        require(positive_sum > 0, 'nonzero original-sum control')
        require(singular_positive > 0, 'nonzero singular-lift control')
        require(lost_nine_negative > 0, 'lost-factor-nine negative control')
        require({-16,0,16} <= offsets, 'both h endpoints and zero')
        # A nonzero depth-13 survivor discovered by the original b=289 control.
        # It is verified directly here, not trusted merely as an expected tuple.
        a, h, length, i = 1, -288, 40932783702951, 141635929767
        require(289*i - a*length == h, 'deep control line')
        require((7*pow(10,length,7**13)-18*pow(10,i,7**13)-25)%(7**13)==0, 'deep control modular predicate')
        pairs, receipt = run(binary, scratch, 17, 289, length, length, 13, 289)
        require((a,h,length,i) in pairs, 'deep positive survivor enumerated')
        require(receipt['pairs22'] == 0, 'deep positive is not full depth22')
        high_pairs, high_receipt = run(binary, scratch, 17, 289, length, length, 22, 289)
        require(high_pairs == [] and high_receipt['pairs22'] == 0, 'full depth22 shift table and lift control')
        # Both inclusive length endpoints are exercised on an actual depth-one pair.
        pairs, _ = run(binary, scratch, 4, 2, 9, 9, 1, 16)
        require((1,-3,9,3) in pairs, 'singleton inclusive endpoints')
    print(json.dumps({'status':'PASS', 'direct_partitions':checks, 'direct_pair_occurrences':all_pairs,
                      'positive_sum_occurrences':positive_sum, 'singular_positive_occurrences':singular_positive, 'lost_nine_negative_occurrences':lost_nine_negative,
                      'direct_stream_sha256':digest.hexdigest(), 'deep_control':[a,h,length,i],
                      'source_sha256':hashlib.sha256(Path(__file__).with_name('independent.cpp').read_bytes()).hexdigest()}, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
