#!/usr/bin/env python3
import re, sys, json
from pathlib import Path

def parse_vm_stats(filename):
    with open(filename) as f:
        content = f.read()

    patterns = {
        'sim_ticks': r'simTicks\s+(\d+)',
        'dtlb_rd_accesses': r'system\.cpu\.mmu\.dtb\.rdAccesses\s+(\d+)',
        'dtlb_rd_misses': r'system\.cpu\.mmu\.dtb\.rdMisses\s+(\d+)',
        'itlb_wr_accesses': r'system\.cpu\.mmu\.itb\.wrAccesses\s+(\d+)',
        'itlb_wr_misses': r'system\.cpu\.mmu\.itb\.wrMisses\s+(\d+)',
    }

    stats = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, content)
        stats[key] = int(match.group(1)) if match else 0

    if stats['dtlb_rd_accesses'] > 0:
        stats['dtlb_miss_rate'] = stats['dtlb_rd_misses'] / stats['dtlb_rd_accesses']

    return stats

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: parse_vm_stats.py <file> or --summary <dir>")
        sys.exit(1)

    if sys.argv[1] == '--summary':
        print(f"{'TLB Size':<10} {'Sim Ticks':<15} {'DTLB Miss %':<12}")
        print("-" * 40)
        for f in sorted(Path(sys.argv[2]).glob('tlb_*_stats.txt')):
            stats = parse_vm_stats(f)
            size = f.stem.split('_')[1].replace('entries', '')
            print(f"{size:<10} {stats['sim_ticks']:<15,} {stats.get('dtlb_miss_rate', 0)*100:<12.2f}")
    else:
        print(json.dumps(parse_vm_stats(sys.argv[1]), indent=2))
