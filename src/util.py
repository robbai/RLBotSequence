from math import copysign
import random
import string


def random_letters(length: int = 10):
    return "".join(random.choice(string.ascii_lowercase) for i in range(length))


def clamp11(val: float):
    return copysign(min(abs(val), 1), val)
