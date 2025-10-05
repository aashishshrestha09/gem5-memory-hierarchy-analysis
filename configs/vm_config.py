#!/usr/bin/env python3
"""
Virtual Memory Configuration Script for gem5
Enables TLB and page size experimentation
"""

import m5
from m5.objects import (
    System, SrcClockDomain, VoltageDomain, AddrRange, X86TimingSimpleCPU,
    L2XBar, Cache, MemCtrl, DDR3_1600_8x8, Process, Root, SystemXBar
)
from m5.util import addToPath
import argparse

def create_vm_system(args):
    """Create system with configurable TLB and page parameters"""

    system = System()

    # Clock configuration
    system.clk_domain = SrcClockDomain()
    system.clk_domain.clock = '3GHz'
    system.clk_domain.voltage_domain = VoltageDomain()

    # Memory configuration
    system.mem_mode = 'timing'
    system.mem_ranges = [AddrRange('2GB')]

    # CPU configuration
    system.cpu = X86TimingSimpleCPU()

    # Configure TLB sizes
    # Data TLB
    system.cpu.mmu.dtb.size = args.dtlb_entries
    # Instruction TLB
    system.cpu.mmu.itb.size = args.itlb_entries

    # L1 Caches
    system.cpu.icache = Cache(
        size=args.l1i_size,
        assoc=2,
        tag_latency=2,
        data_latency=2,
        response_latency=1,
        mshrs=4,
        tgts_per_mshr=20
    )

    system.cpu.dcache = Cache(
        size=args.l1d_size,
        assoc=2,
        tag_latency=2,
        data_latency=2,
        response_latency=1,
        mshrs=4,
        tgts_per_mshr=20
    )


    # L2 bus
    system.l2bus = L2XBar()

    # Connect L1 caches to CPU and L2 bus
    system.cpu.icache_port = system.cpu.icache.cpu_side
    system.cpu.dcache_port = system.cpu.dcache.cpu_side
    system.cpu.icache.mem_side = system.l2bus.cpu_side_ports
    system.cpu.dcache.mem_side = system.l2bus.cpu_side_ports

    # L2 Cache
    system.l2cache = Cache(
        size=args.l2_size,
        assoc=8,
        tag_latency=20,
        data_latency=20,
        response_latency=1,
        mshrs=20,
        tgts_per_mshr=12
    )
    system.l2cache.cpu_side = system.l2bus.mem_side_ports

    # Memory bus
    system.membus = SystemXBar()
    system.l2cache.mem_side = system.membus.cpu_side_ports


    # Memory controller with page size awareness
    system.mem_ctrl = MemCtrl()
    system.mem_ctrl.dram = DDR3_1600_8x8()
    system.mem_ctrl.dram.range = system.mem_ranges[0]
    system.mem_ctrl.port = system.membus.mem_side_ports

    # System port
    system.system_port = system.membus.cpu_side_ports

    # Interrupt controller
    system.cpu.createInterruptController()
    system.cpu.interrupts[0].pio = system.membus.mem_side_ports
    system.cpu.interrupts[0].int_master = system.membus.cpu_side_ports
    system.cpu.interrupts[0].int_slave = system.membus.mem_side_ports

    return system

def main():
    parser = argparse.ArgumentParser(
        description='gem5 Virtual Memory Configuration Experiment'
    )

    # Benchmark program
    parser.add_argument('--binary', required=True,
                       help='Binary to execute')

    # TLB configuration
    parser.add_argument('--dtlb_entries', type=int, default=64,
                       help='Data TLB entry count')
    parser.add_argument('--itlb_entries', type=int, default=64,
                       help='Instruction TLB entry count')

    # Cache configuration (kept for consistency)
    parser.add_argument('--l1i_size', default='32kB')
    parser.add_argument('--l1d_size', default='32kB')
    parser.add_argument('--l2_size', default='256kB')

    args = parser.parse_args()


    # Create system
    system = create_vm_system(args)

    # Set up workload for syscall emulation (like cache_config.py)
    import os
    from m5.objects import SEWorkload
    binary_path = args.binary
    if not os.path.isabs(binary_path):
        binary_path = os.path.abspath(binary_path)
    system.workload = SEWorkload.init_compatible(binary_path)

    # Set up process
    process = Process()
    process.cmd = [binary_path]
    system.cpu.workload = process
    system.cpu.createThreads()

    # Instantiate and run
    root = Root(full_system=False, system=system)
    m5.instantiate()

    print(f"gem5 Virtual Memory Experiment")
    print(f"Configuration:")
    print(f"  Data TLB entries:   {args.dtlb_entries}")
    print(f"  Instr TLB entries:  {args.itlb_entries}")
    print(f"  L1D Cache:          {args.l1d_size}")
    print(f"  L2 Cache:           {args.l2_size}")
    print(f"Starting simulation...")

    exit_event = m5.simulate()

    print(f'\nSimulation Complete')
    print(f'Total Ticks: {m5.curTick()}')
    print(f'Exit Cause: {exit_event.getCause()}')

if __name__ == "__m5_main__":
    main()

