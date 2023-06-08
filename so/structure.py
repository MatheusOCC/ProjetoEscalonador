import random


def word():
    return f"{random.randint(0,255):08b}"


class Address:
    def __init__(self, pos, value="", pag=''):
        self.pos = pos
        self.value = f"{0:08b}"
        self.page = pag

    def __str__(self):
        return f"{self.page:08b}" + self.value


class VirtualPage:
    def __init__(self, number, size):
        self.start = number * size
        self.addresses = [Address(i + self.start, pag=number) for i in range(size)]
        self.number = number
        self.empty = True

    def add_data(self, page):
        for address, data in zip(self.addresses, page.data):
            address.value = data
        self.empty = False

    def remove_data(self):
        for address in self.addresses:
            address.value = ""
        self.empty = True


class Frame:
    def __init__(self, number, size, t=0):
        self.start = number * size
        self.addresses = [Address(i + self.start, pag=number) for i in range(size)]
        self.number = number
        self.empty = True
        self.t = t
        self.r = 0
        self.m = 0

    def add_data(self, v_page, t):
        for f_address, v_address in zip(self.addresses, v_page.addresses):
            f_address.value = v_address.value
        self.t = t
        self.empty = False

    def update_bits(self, r, m):
        self.r = r
        self.m = m

    def remove_data(self):
        for address in self.addresses:
            address.value = ""
        self.t = 0
        self.empty = True


class Page:
    def __init__(self, size, data=None):
        self.data = data
        self.size = size
        self.virtual_page = None
        if not data:
            self.add_data()

    def add_data(self):
        self.data = [word() for line in range(self.size)]
