# Assignment 3: Exploring Memory Hierarchy Design in gem5

## Repository Overview

This repository contains complete experimental framework for investigating memory hierarchy design using the gem5 simulator. The study explores cache configuration optimizations and virtual memory performance characteristics through systematic experimentation.

## Repository Structure

```text
.
├── configs
│   ├── cache_config.py
│   └── vm_config.py
├── docs
├── README.md
├── results
│   ├── cache_experiments
│   │   ├── assoc_1way_stats.txt
│   │   ├── assoc_4way_stats.txt
│   │   ├── assoc_8way_stats.txt
│   │   ├── baseline_stats.txt
│   │   ├── l1d_128kB_stats.txt
│   │   ├── l1d_16kB_stats.txt
│   │   ├── l1d_64kB_stats.txt
│   │   ├── l2_128kB_stats.txt
│   │   ├── l2_1MB_stats.txt
│   │   └── l2_512kB_stats.txt
│   └── vm_experiments
│       ├── tlb_128entries_stats.txt
│       ├── tlb_16entries_stats.txt
│       ├── tlb_256entries_stats.txt
│       ├── tlb_32entries_stats.txt
│       └── tlb_64entries_stats.txt
├── scripts
│   ├── parse_stats.py
│   ├── parse_vm_stats.py
│   ├── run_all_experiments.sh
│   ├── run_cache_experiments.sh
│   └── run_vm_experiments.sh
└── src
    ├── matrix_multi.c
    └── matrix_multi.txt

8 directories, 25 files
```

## Prerequisites

- **gem5 Simulator:** Version 25.0.0.1 or later
- **Compiler:** GCC for x86_64 with static linking support
- **Python:** Version 3.8 or higher
- **Operating System:** Linux (or macOS with container support)

## Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/aashishshrestha09/gem5-memory-hierarchy-analysis.git
cd gem5-memory-hierarchy-analysis
```

### 2. Compile Benchmark

```bash
cd src
gcc -static -O2 -o matrix_multi matrix_multi.c
cd ..
```

### 3. Run All Experiments

```bash
chmod +x scripts/*.sh
./scripts/run_all_experiments.sh
```

## Detailed Experiment Instructions

### Cache Configuration Experiments

**_Individual Cache Size Tests_**

```bash
# 16kB L1D cache
build/X86/gem5.opt configs/cache_config.py \
 --cmd=src/matrix_multi \
 --l1d_size=16kB --l1i_size=32kB \
 --l2_size=256kB

# 64kB L1D cache
build/X86/gem5.opt configs/cache_config.py \
 --cmd=src/matrix_multi \
 --l1d_size=64kB --l1i_size=32kB \
 --l2_size=256kB
```

**_Associativity Tests_**

```bash
# Direct-mapped (1-way)
build/X86/gem5.opt configs/cache_config.py \
 --cmd=src/matrix_multi \
 --l1d_assoc=1

# 4-way set-associative
build/X86/gem5.opt configs/cache_config.py \
 --cmd=src/matrix_multi \
 --l1d_assoc=4
```

**_Run All Cache Experiments_**

```bash
./scripts/run_cache_experiments.sh
```

## Virtual Memory Experiments

### TLB Sizing Tests

```bash
# 32-entry TLB
build/X86/gem5.opt configs/vm_config.py \
 --cmd=src/matrix_multi \
 --dtlb_entries=32 --itlb_entries=32

# 128-entry TLB
build/X86/gem5.opt configs/vm_config.py \
 --cmd=src/matrix_multi \
 --dtlb_entries=128 --itlb_entries=128
```

### Run All VM Experiments

```bash
./scripts/run_vm_experiments.sh
```

## Results Analysis

### Parse Cache Statistics

```bash
# Individual file
./scripts/parse_stats.py results/cache_experiments/baseline_stats.txt

# Generate summary
./scripts/parse_stats.py --summary results/cache_experiments
```

### Parse VM Statistics

```bash
# Individual file
./scripts/parse_vm_stats.py results/vm_experiments/tlb_64entries_stats.txt

# Generate summary table
./scripts/parse_vm_stats.py --summary results/vm_experiments
```
