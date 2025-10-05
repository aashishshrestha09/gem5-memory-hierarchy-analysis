#!/bin/bash
# Virtual memory TLB experiments

RESULTS_DIR="results/vm_experiments"
mkdir -p $RESULTS_DIR

GEM5="gem5-mesi"
VM_CONFIG="configs/vm_config.py"
BENCHMARK="src/matrix_multi"

echo "======================================"
echo "Virtual Memory TLB Experiments"
echo "======================================"

for size in 16 32 64 128 256; do
    echo "TLB entries=$size..."
    $GEM5 $VM_CONFIG --binary=$BENCHMARK \
      --dtlb_entries=$size --itlb_entries=$size
    cp m5out/stats.txt $RESULTS_DIR/tlb_${size}entries_stats.txt
done

echo "VM experiments complete!"
