#!/usr/bin/env python3
import re, sys, json
from pathlib import Path

def parse_stats(filename):
    with open(filename) as f:
        content = f.read()

    patterns = {
        'sim_ticks': r'simTicks\s+(\d+)',
        'l1d_hits': r'system\.cpu\.dcache\.demandHits::total\s+(\d+)',
        'l1d_misses': r'system\.cpu\.dcache\.demandMisses::total\s+(\d+)',
        'l2_hits': r'system\.l2cache\.demandHits::total\s+(\d+)',
        'l2_misses': r'system\.l2cache\.demandMisses::total\s+(\d+)',
    }

    stats = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, content)
        stats[key] = int(match.group(1)) if match else 0

    if stats['l1d_hits'] + stats['l1d_misses'] > 0:
        stats['l1d_miss_rate'] = stats['l1d_misses'] / (stats['l1d_hits'] + stats['l1d_misses'])

    return stats

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: parse_stats.py <file> or --summary <dir>")
        sys.exit(1)

    if sys.argv[1] == '--summary':
        for f in sorted(Path(sys.argv[2]).glob('*.txt')):
            print(f"\n{f.name}:")
            print(json.dumps(parse_stats(f), indent=2))
    else:
        print(json.dumps(parse_stats(sys.argv[1]), indent=2))
