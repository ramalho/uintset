import array
import random

class Fixture():

    def __init__(self, desired_len, desired_density):
        data = list(range(desired_len))
        random.shuffle(data)
        self._data = array.array('Q', data)
        self._max_uint = desired_len

    def __len__(self):
        return len(self._data)

    def density(self):
        s = set(self._data)
        found = 0
        for i in range(self._max_uint):
            if i in s:
                found += 1
        return found / len(self)
