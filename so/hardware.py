import numpy as np
import random
from structure import VirtualPage, Frame, Page
from visual import TColors
from hardware_functions import modify, process_sort

K = 1024
TIME = 0


def print_time():
    global TIME
    print(f"{TColors.BOLD}TIME: {TIME}{TColors.ENDC}")


class MMU:
    def __init__(self, disk):
        self.mem_map = {value: None for value in range(disk.n_virtual_pages)}

    def virtual_to_physical(self, disk_page):
        return self.mem_map[disk_page]

    def physical_to_virtual(self, ram_page):
        return list(self.mem_map.keys())[list(self.mem_map.values()).index(ram_page)]

    def update_map(self, disk_page, ram_page, add=True):
        if add:
            self.mem_map[disk_page] = ram_page
        else:
            disk_page = self.physical_to_virtual(ram_page)
            self.mem_map[disk_page] = None


class Process:
    def __init__(
        self,
        arrival,
        duration,
        quantum=2,
        n_pages=10,
        pid=None,
        overload=1,
        priority=0,
        deadline=None,
    ):
        self.arrival = arrival
        self.duration = duration
        self.deadline = deadline
        self.duration = duration
        self.priority = priority  # Validar Prioridade
        self.quantum = quantum  # Validar Quantum
        self.overload = overload  # Validar Sobrecarga
        self.runtime = 0
        if(not pid):
            self.id = random.randint(100, 999)
        else:
            self.id = pid
        self.page_size = 4 * K  # 4k
        self.n_pages = n_pages
        self.pages = [
            Page(self.page_size) for i in range(self.n_pages)
        ]  # Validar número de Páginas
        self.endtime = None
        self.n_pages_in_disk = 0
        self.running_time = []
        self.overload_time = []
        self.paging_time = []

    def __str__(self):
        return f"Process {self.id}"

    def info(self):
        print(
            f"{self.__str__()} - Arrival: {self.arrival} | Duration: {self.duration} | Deadline: {self.deadline} | Nº Pages: {self.n_pages} "
        )

    def pages_in_disk(self, mmu):
        pages = [
            page
            for page in self.pages
            if mmu.virtual_to_physical(page.virtual_page) is None
        ]
        self.n_pages_in_disk = len(pages)
        return pages

    def pages_in_ram(self, mmu):
        frames = [
            mmu.virtual_to_physical(page.virtual_page)
            for page in self.pages
            if mmu.virtual_to_physical(page.virtual_page) is not None
        ]
        return frames

    def in_ram(self, mmu):
        self.pages_in_disk(mmu)
        return None not in [
            mmu.virtual_to_physical(page.virtual_page) for page in self.pages
        ]

    def overload_store(self):
        global TIME
        self.overload_time.append(TIME)

    def run(self):
        global TIME
        if not self.was_finished():
            self.runtime += 1
            self.running_time.append(TIME)
            TIME += 1
            print(f"{self.__str__()} is running...")
        else:
            print(f"{self.__str__()} is finished!")

    def modify(self):
        pass

    def was_finished(self):
        global TIME
        if self.runtime >= self.duration:
            self.endtime = TIME - 1
        return self.runtime >= self.duration


class Disk:
    def __init__(self):
        self.disk_size = 1000 * K  # 100k
        self.virtual_page_size = 4 * K  # 4k
        self.n_virtual_pages = self.disk_size // self.virtual_page_size  # 250
        self.virtual_pages = [
            VirtualPage(n, self.virtual_page_size) for n in range(self.n_virtual_pages)
        ]
        self.n_empty_virtual_pages = len(self.empty_pages())

    def empty_pages(self):
        return [page for page in self.virtual_pages if page.empty]

    def check(self, n_pages):
        return self.n_empty_virtual_pages >= n_pages

    def update_pages(self):
        self.n_empty_virtual_pages = len(self.empty_pages())

    def clean_disk(self):
        self.virtual_pages = [
            VirtualPage(n, self.virtual_page_size) for n in range(self.n_virtual_pages)
        ]
        self.update_pages()

    def allocate_process(self, process):
        if self.check(process.n_pages):
            for pag, virtual_page in zip(process.pages, self.empty_pages()):
                virtual_page.add_data(pag)
                pag.virtual_page = virtual_page.number
            self.update_pages()
            return True
        else:
            return False


class RAM:
    def __init__(self, method="fifo"):
        self.ram_size = 200 * K  # 200k
        self.frame_size = 4 * K  # 4k
        self.n_frames = self.ram_size // self.frame_size  # 50
        self.frames = [Frame(n, self.frame_size) for n in range(self.n_frames)]
        self.n_empty_frames = len(self.empty_frames())
        self.method = method

    def empty_frames(self):
        return [frame for frame in self.frames if frame.empty]

    def used_frames(self):
        return [frame for frame in self.frames if not frame.empty]

    def check(self, n_pages):
        self.update_frames()
        return self.n_empty_frames >= n_pages

    def update_frames(self):
        self.n_empty_frames = len(self.empty_frames())

    def clean_ram(self):
        self.frames = [Frame(n, self.frame_size) for n in range(self.n_frames)]
        self.update_frames()

    def allocate_process(self, process, disk, mmu):
        global TIME
        self.update_frames()
        if self.check(process.n_pages_in_disk):
            virtual_pages = [pag.virtual_page for pag in process.pages_in_disk(mmu)]
            for v_pag, frame in zip(virtual_pages, self.empty_frames()):
                f_pag = mmu.virtual_to_physical(v_pag)
                if f_pag is not None:
                    print(f"This page is on RAM, frame: nº{f_pag}")
                else:
                    frame.add_data(disk.virtual_pages[v_pag], TIME)
                    mmu.update_map(v_pag, frame.number)
            print_time()
            print(f"{process.__str__()} was allocated on RAM!")
            self.update_frames()
            return True
        else:
            print(f"There is no space left on RAM for {process.__str__()}!")
            process.pages_in_disk(mmu)
            return False

    def paging(self, process, mmu, disk):
        global TIME
        process_frames = process.pages_in_ram(mmu)
        process.pages_in_disk(mmu)
        n_remove = process.n_pages_in_disk - self.n_empty_frames
        for i in range(n_remove):
            if self.method == "fifo":
                self.fifo(mmu, process_frames)
            elif self.method == "nru":
                self.nru(mmu, process_frames)
        process.pages_in_disk(mmu)
        process.paging_time.append(TIME)
        TIME += 1
        print(f"{n_remove} pages were removed from RAM!")
        self.allocate_process(process, disk, mmu)

    def remove_frame(self, frame, mmu):
        frame.remove_data()
        mmu.update_map(None, frame.number, False)
        self.update_frames()

    def update_disk(self, frame, disk):
        pass

    def fifo(self, mmu, process_frames):  # First In First Out
        frames = [
            frame
            for frame in self.used_frames()
            if frame.number not in process_frames
        ]
        first_frame = frames[np.argmin([frame.t for frame in frames])]
        first_pos = self.used_frames().index(first_frame)
        self.remove_frame(self.used_frames()[first_pos], mmu)
        return True

    def nru(self, mmu, process_frames):  # Not Recently Used
        c0, c1, c2, c3 = [], [], [], []
        remove = None
        frames = [
            frame
            for frame in self.used_frames()
            if frame.number not in process_frames
        ]
        for frame in frames:
            if frame.r == 0 and frame.m == 0:  # Not Referenced, Not Modified
                c0.append(frame)
            elif frame.r == 0 and frame.m == 1:  # Not Referenced, Modified
                c1.append(frame)
            elif frame.r == 1 and frame.m == 0:  # Referenced, Not Modified
                c2.append(frame)
            elif frame.r == 1 and frame.m == 1:  # Referenced, Modified
                c3.append(frame)
        if c0:
            remove = random.choice(c0)
        elif c1:
            remove = random.choice(c1)
        elif c2:
            remove = random.choice(c2)
        elif c3:
            remove = random.choice(c3)
        nru_pos = self.used_frames().index(remove)
        self.remove_frame(self.used_frames()[nru_pos], mmu)
        return True


class CPU:
    def __init__(self, ram, mmu, disk, processes=[], quantum=0):
        self.processes = processes
        self.curr_processes = []
        self.quantum = quantum
        self.ram = ram
        self.mmu = mmu
        self.disk = disk

    def add_process(self, process):
        self.processes.append(process)
        print(f"{TColors.GREEN}{process.__str__()} was added!{TColors.ENDC}")
        return True

    def remove_process(self, process):
        self.curr_processes.remove(process)
        print(f"{TColors.RED}{process.__str__()} was finished!{TColors.ENDC}")
        return True

    def overload(self, overload=1):
        global TIME
        TIME += overload
        print(f"{TColors.BOLD}{TColors.RED}OVERLOAD\n{TColors.ENDC}")
        return True

    def check_arrival(self):
        global TIME
        swap = []
        arrival = False
        for process in self.processes:
            # if process.arrival == TIME:
            if process.arrival <= TIME:
                arrival = True
                swap.append(process)
        for process in swap:
            self.processes.remove(process)
            self.curr_processes.append(process)
            print_time()
            print(f"{TColors.YELLOW}{process.__str__()} has arrived!{TColors.ENDC}")
            self.ram.update_frames()
            #  self.ram.allocate_process(process, self.disk, self.mmu)
        return arrival

    def move_to_end(self, process):
        self.curr_processes.append(process)
        self.curr_processes.remove(process)

    def update_bits(self, process, r, m):
        virtual_pages = [pag.virtual_page for pag in process.pages]
        physical_frames = [
            self.mmu.virtual_to_physical(address) for address in virtual_pages
        ]
        for frame in physical_frames:
            self.ram.frames[frame].update_bits(r, m)

    def print_processes(self):
        for process in self.curr_processes:
            print(f"{process.__str__()}", end=" | ")
        print()

    def verify_ram(self, process):
        if not process.in_ram(self.mmu):
            if not self.ram.allocate_process(process, self.disk, self.mmu):
                process.pages_in_disk(self.mmu)
                self.ram.paging(process, self.mmu, self.disk)

    def fifo(self):  # First In First Out
        global TIME
        m = 0
        while self.processes or self.curr_processes:
            self.check_arrival()
            if self.curr_processes:  # Existe ao menos um processo para rodar
                order_of_arrival = process_sort(self.curr_processes, "arrival")
                for process in order_of_arrival:
                    while not process.was_finished():
                        self.verify_ram(process)
                        m = modify()
                        self.update_bits(
                            process, 1, m
                        )  # Referenciado e talvez Modificado
                        print_time()
                        process.run()
                        self.check_arrival()
                    self.update_bits(process, 0, m)  # Não Referenciado mais
                    self.remove_process(process)
            else:  # Não há processos ainda
                print_time()
                TIME += 1
        print_time()

    def sjf(self):  # Shorst Job First
        global TIME
        m = 0
        while self.processes or self.curr_processes:
            self.check_arrival()
            if self.curr_processes:  # Existe ao menos um processo para rodar
                order_of_duration = process_sort(self.curr_processes, "duration")
                for process in order_of_duration:
                    while not process.was_finished():
                        self.verify_ram(process)
                        m = modify()
                        self.update_bits(
                            process, 1, m
                        )  # Referenciado e talvez Modificado
                        print_time()
                        process.run()
                        self.check_arrival()
                    m = modify()
                    self.update_bits(process, 0, m)  # Não Referenciado mais
                    self.remove_process(process)
            else:  # Não há processos ainda
                print_time()
                TIME += 1
        print_time()

    def rr(self):  # Round Robin
        global TIME
        m = 0
        while self.processes or self.curr_processes:
            self.check_arrival()
            if self.curr_processes:  # Existe ao menos um processo para rodar
                while self.curr_processes:
                    overload = False
                    for process in self.curr_processes[
                        :
                    ]:  # Copiar a lista original para poder remover
                        for time in range(process.quantum):
                            if time == process.quantum - 1:  # Ultimo quantum
                                self.verify_ram(process)
                                m = modify()
                                self.update_bits(
                                    process, 1, m
                                )  # Referenciado e talvez Modificado
                                print_time()
                                process.run()
                                self.check_arrival()
                                if (
                                    process.was_finished()
                                ):  # Verificar se foi finalizado antes do overload
                                    self.update_bits(
                                        process, 0, m
                                    )  # Não Referenciado mais
                                    self.remove_process(process)
                                    break
                                print_time()
                                process.overload_store()
                                overload = self.overload()  # Aplicar overload
                                self.check_arrival()  # Verificar se há um novo processo
                                self.move_to_end(
                                    process
                                )  # Mover o processo para o fim da fila
                                self.update_bits(process, 0, m)  # Não Referenciado mais
                                break
                            else:  # Quantum Normal
                                self.verify_ram(process)
                                m = modify()
                                self.update_bits(
                                    process, 1, m
                                )  # Referenciado e talvez Modificado
                                print_time()
                                process.run()
                                self.check_arrival()
                                if process.was_finished():  # Verificar se foi finalizado
                                    self.update_bits(
                                        process, 0, m
                                    )  # Não Referenciado mais
                                    self.remove_process(process)
                                    break
                        if process.was_finished() or overload:
                            break
            else:  # Não há processos ainda
                print_time()
                TIME += 1
        print_time()

    def edf(self):
        global TIME
        m = 0
        while self.processes or self.curr_processes:
            self.check_arrival()
            if self.curr_processes:  # Existe ao menos um processo para rodar
                order_of_deadline = process_sort(self.curr_processes, "deadline")
                for process in order_of_deadline:
                    overload = False
                    while not process.was_finished():
                        for time in range(process.quantum):
                            if time == process.quantum - 1:  # Ultimo quantum
                                self.verify_ram(process)
                                m = modify()
                                self.update_bits(
                                    process, 1, m
                                )  # Referenciado e talvez Modificado
                                print_time()
                                process.run()
                                self.check_arrival()
                                if (
                                    process.was_finished()
                                ):  # Verificar se foi finalizado antes do overload
                                    self.update_bits(
                                        process, 0, m
                                    )  # Não Referenciado mais
                                    self.remove_process(process)
                                    break
                                print_time()
                                process.overload_store()
                                overload = self.overload()  # Aplicar overload
                                self.check_arrival()
                                break
                            else:  # Quantum Normal
                                self.verify_ram(process)
                                m = modify()
                                self.update_bits(
                                    process, 1, m
                                )  # Referenciado e talvez Modificado
                                print_time()
                                process.run()
                                self.check_arrival()
                                if process.was_finished():  # Verificar se foi finalizado
                                    self.update_bits(
                                        process, 0, m
                                    )  # Não Referenciado mais
                                    self.remove_process(process)
                                    break
                        if process.was_finished() or overload:
                            break
                    if process.was_finished() or overload:
                        break
            else:  # Não há processos ainda
                print_time()
                TIME += 1
        print_time()
