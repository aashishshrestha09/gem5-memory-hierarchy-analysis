from m5.objects import (
    System, SrcClockDomain, VoltageDomain, AddrRange, X86TimingSimpleCPU,
    Cache, L2XBar, SystemXBar, MemCtrl, DDR3_1600_8x8, SEWorkload, Process, Root
)
import m5
import argparse
import m5
import argparse

# -------------------------------
# Command-line arguments
# -------------------------------
parser = argparse.ArgumentParser(description='gem5 Cache Simulation Script')
parser.add_argument('--l1d-size', default='32kB', help='L1 Data Cache Size')
parser.add_argument('--l1i-size', default='32kB', help='L1 Instruction Cache Size')
parser.add_argument('--l2-size', default='256kB', help='L2 Cache Size')
parser.add_argument('--l1-assoc', type=int, default=2, help='L1 Associativity')
parser.add_argument('--l2-assoc', type=int, default=8, help='L2 Associativity')
parser.add_argument('--cacheline-size', type=int, default=64, help='Cache Line Size')
parser.add_argument('--binary', required=True, help='Binary to execute')
parser.add_argument('--dtlb-entries', type=int, default=64, help='Data TLB Entries')
parser.add_argument('--itlb-entries', type=int, default=64, help='Instruction TLB Entries')
args = parser.parse_args()

# -------------------------------
# Cache definitions
# -------------------------------
class L1DCache(Cache):
    size = args.l1d_size
    assoc = args.l1_assoc
    tag_latency = 2
    data_latency = 2
    response_latency = 2
    mshrs = 4
    tgts_per_mshr = 20
    writeback_clean = False

class L1ICache(Cache):
    size = args.l1i_size
    assoc = args.l1_assoc
    tag_latency = 2
    data_latency = 2
    response_latency = 2
    mshrs = 4
    tgts_per_mshr = 20
    writeback_clean = False

class L2Cache(Cache):
    size = args.l2_size
    assoc = args.l2_assoc
    tag_latency = 20
    data_latency = 20
    response_latency = 20
    mshrs = 20
    tgts_per_mshr = 12
    writeback_clean = False

# -------------------------------
# System configuration
# -------------------------------
system = System()
system.clk_domain = SrcClockDomain(clock='3GHz', voltage_domain=VoltageDomain())
system.mem_mode = 'timing'
system.mem_ranges = [AddrRange('512MB')]

# CPU
system.cpu = X86TimingSimpleCPU()

# TLB configuration

# -------------------------------
# Cache hierarchy
# -------------------------------
# L2 bus and cache
system.l2bus = L2XBar()
# L1 caches
system.cpu.icache = L1ICache()
system.cpu.dcache = L1DCache()
# Explicitly connect CPU cache ports to L1 caches
system.cpu.icache_port = system.cpu.icache.cpu_side
system.cpu.dcache_port = system.cpu.dcache.cpu_side
# Connect L1 caches to L2 bus
system.cpu.icache.mem_side = system.l2bus.cpu_side_ports
system.cpu.dcache.mem_side = system.l2bus.cpu_side_ports
# L2 cache sits between L2 bus and memory bus
system.l2cache = L2Cache()
system.l2cache.cpu_side = system.l2bus.mem_side_ports
system.membus = SystemXBar()
system.l2cache.mem_side = system.membus.cpu_side_ports

# Memory controller
system.mem_ctrl = MemCtrl(dram=DDR3_1600_8x8(range=system.mem_ranges[0]))
system.mem_ctrl.port = system.membus.mem_side_ports

# System port
system.system_port = system.membus.cpu_side_ports

# Interrupts (x86)
system.cpu.createInterruptController()
system.cpu.interrupts[0].pio = system.membus.mem_side_ports
system.cpu.interrupts[0].int_requestor = system.membus.cpu_side_ports
system.cpu.interrupts[0].int_responder = system.membus.mem_side_ports

# -------------------------------
# Workload configuration
# -------------------------------
binary = args.binary
system.workload = SEWorkload.init_compatible(binary)

process = Process()
process.cmd = [binary]
system.cpu.workload = process
system.cpu.createThreads()

# -------------------------------
# Instantiate and run
# -------------------------------
root = Root(full_system=False, system=system)
m5.instantiate()

print(f"Starting simulation with:")
print(f"  L1D: {args.l1d_size}, L1I: {args.l1i_size}, L2: {args.l2_size}")
print(f"  L1 Assoc: {args.l1_assoc}, L2 Assoc: {args.l2_assoc}")
print(f"  Cache Line: {args.cacheline_size}B")
print(f"  DTLB: {args.dtlb_entries}, ITLB: {args.itlb_entries}")

exit_event = m5.simulate()
print(f'\nExiting @ tick {m5.curTick()} because {exit_event.getCause()}')
print("\nSimulation Complete! Stats in m5out/stats.txt")
