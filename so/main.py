from functions import processes_df, turnaround
from hardware import Disk, CPU, RAM, MMU, Process
from visual import process_fig

PAGING_METHOD = "fifo"
CPU_METHOD = "edf"

processes = [
    Process(arrival=9, duration=9, pid=1, deadline=62, n_pages=5),
    Process(arrival=2, duration=11, pid=2, deadline=82, n_pages=8),
    Process(arrival=4, duration=8, pid=3, deadline=38, n_pages=5),
    Process(arrival=7, duration=14, pid=4, deadline=82, n_pages=4),
    Process(arrival=0, duration=18, pid=5, deadline=72, n_pages=9),
    Process(arrival=2, duration=19, pid=6, deadline=71, n_pages=7),
    Process(arrival=2, duration=13, pid=7, deadline=90, n_pages=10),
    Process(arrival=10, duration=9, pid=8, deadline=65, n_pages=6),
    Process(arrival=3, duration=16, pid=9, deadline=59, n_pages=9),
    Process(arrival=3, duration=16, pid=10, deadline=54, n_pages=8),
]

disk = Disk()
ram = RAM(method=PAGING_METHOD)
mmu = MMU(disk)
cpu = CPU(ram, mmu, disk)
for p in processes:
    disk.allocate_process(p)
    cpu.add_process(p)
exec(f"cpu.{CPU_METHOD}()")

df = processes_df(processes)
print(f"Turnaround Médio = {turnaround(processes)}")
process_fig(df, processes, f"{CPU_METHOD}_{PAGING_METHOD}_{turnaround(processes)}")
