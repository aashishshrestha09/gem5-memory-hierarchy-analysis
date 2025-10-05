#!/bin/bash
# Cache configuration experiments

RESULTS_DIR="results/cache_experiments"
mkdir -p $RESULTS_DIR

GEM5="gem5-mesi"
CONFIG="configs/cache_config.py"
BENCHMARK="src/matrix_multi"

echo "======================================"
echo "Cache Configuration Experiments"
echo "======================================"

# Baseline
echo "Running baseline (32kB L1, 256kB L2)..."
$GEM5 $CONFIG --binary=$BENCHMARK \
  --l1d-size=32kB --l1i-size=32kB --l2-size=256kB \
  --l1-assoc=2 --l2-assoc=8
cp m5out/stats.txt $RESULTS_DIR/baseline_stats.txt

# L1D Size Sweep
for size in 16kB 64kB 128kB; do
    echo "L1D size=$size..."
    $GEM5 $CONFIG --binary=$BENCHMARK --l1d-size=$size \
      --l1i-size=32kB --l2-size=256kB --l1-assoc=2 --l2-assoc=8
    cp m5out/stats.txt $RESULTS_DIR/l1d_${size}_stats.txt
done

# L2 Size Sweep
for size in 128kB 512kB 1MB; do
    echo "L2 size=$size..."
    $GEM5 $CONFIG --binary=$BENCHMARK --l2-size=$size \
      --l1d-size=32kB --l1i-size=32kB --l1-assoc=2 --l2-assoc=8
    cp m5out/stats.txt $RESULTS_DIR/l2_${size}_stats.txt
done

# Associativity Sweep
for assoc in 1 4 8; do
    echo "L1D assoc=$assoc-way..."
    $GEM5 $CONFIG --binary=$BENCHMARK --l1-assoc=$assoc \
      --l1d-size=32kB --l1i-size=32kB --l2-size=256kB --l2-assoc=8
    cp m5out/stats.txt $RESULTS_DIR/assoc_${assoc}way_stats.txt
done

echo "Cache experiments complete!"
