#!/bin/bash
# Master script to run all experiments

set -e  # Exit on error

echo "=========================================="
echo "Assignment 3: Complete Experiment Suite"
echo "=========================================="
echo ""

# Check if benchmark exists
if [ ! -f "./src/matrix_multi" ]; then
    echo "ERROR: Benchmark not found"
    echo "Compiling benchmark..."
    gcc -static -O2 -o ./src/matrix_multi ./src/matrix_multi.c
fi

# Create results directories
mkdir -p results/cache_experiments
mkdir -p results/vm_experiments

echo "Starting cache experiments..."
./scripts/run_cache_experiments.sh

echo ""
echo "Starting virtual memory experiments..."
./scripts/run_vm_experiments.sh

echo ""
echo "=========================================="
echo "All experiments complete!"
echo "=========================================="
echo ""
echo "Results location:"
echo "  Cache:   results/cache_experiments/"
echo "  VM:      results/vm_experiments/"
echo ""
echo "To analyze results:"
echo "  ./scripts/parse_stats.py --summary results/cache_experiments"
echo "  ./scripts/parse_vm_stats.py --summary results/vm_experiments"
