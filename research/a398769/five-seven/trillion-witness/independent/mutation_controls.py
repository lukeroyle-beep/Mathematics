#!/usr/bin/env python3
"""Show that the independent stream audit rejects deliberate certificate damage."""
import argparse
import copy
import gzip
import hashlib
import json
from pathlib import Path
import tempfile
from verify_digits import require
from verify_stream import HEADER, read_stream


def run(path):
    opener = gzip.open if path.suffix == '.gz' else open
    with opener(path, 'rt') as source:
        require(source.readline().rstrip('\n').split('\t') == HEADER, 'bad source header')
        rows = [source.readline().rstrip('\n').split('\t') for _ in range(20)]
    require(all(len(row) == 8 for row in rows), 'need twenty control rows')
    start, stop = int(rows[0][0]), int(rows[-1][0])
    actual_index = next(j for j,row in enumerate(rows) if row[3] != 'outside')
    cases = []
    def mutate(label, index, field, value):
        altered = copy.deepcopy(rows)
        altered[index][field] = str(value)
        cases.append((label, altered))
    mutate('gap_or_duplicate_length', 1, 0, start)
    mutate('wrong_representative', actual_index, 2, int(rows[actual_index][2])+1)
    mutate('wrong_K', actual_index, 1, int(rows[actual_index][1])+1)
    mutate('wrong_sum_residue', actual_index, 5, int(rows[actual_index][5])+9)
    mutate('wrong_seven_residue', actual_index, 6, int(rows[actual_index][6])+1)
    mutate('wrong_exact_depth', actual_index, 4, int(rows[actual_index][4])+1)
    mutate('wrong_lift_digit', actual_index, 7, int(rows[actual_index][7]) % 6+1)
    mutate('wrong_category', actual_index, 3, 'outside')
    cases.append(('truncated_certificate', rows[:-1]))
    outcomes = []
    with tempfile.TemporaryDirectory(prefix='trillion-independent-mutations-') as directory:
        target = Path(directory)/'control.tsv'
        def write(changed):
            target.write_text('\t'.join(HEADER)+'\n'+''.join('\t'.join(row)+'\n' for row in changed))
        write(rows)
        control = read_stream(target, start, stop)
        require(control['status'] == 'PASS', 'undamaged prefix must pass')
        for label, altered in cases:
            write(altered)
            try:
                read_stream(target, start, stop)
            except ValueError as error:
                outcomes.append({'mutation': label, 'rejected': True, 'reason': str(error)})
            else:
                raise ValueError('mutation was accepted: '+label)
    return {'status': 'PASS', 'undamaged_prefix_rows': len(rows),
            'mutations_rejected': len(outcomes), 'outcomes': outcomes,
            'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'stream_verifier_sha256': hashlib.sha256(Path(__file__).with_name('verify_stream.py').read_bytes()).hexdigest()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('certificate', type=Path)
    args = parser.parse_args()
    print(json.dumps(run(args.certificate), indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
