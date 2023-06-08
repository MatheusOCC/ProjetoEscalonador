from visual import TColors
import numpy as np
from operator import attrgetter


def modify():
    return np.random.choice([0, 1], p=[0.8, 0.2])


def process_sort(process_list: list, attribute: str, asceding: bool = False):
    return sorted(process_list, key=attrgetter(attribute), reverse=asceding)
