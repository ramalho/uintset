import array


class UintSet():

    def __init__(self, it=None):
        self.words = array.array('I')
        self.len = 0
        if it is not None:
            for i in it:
                self.add(i)

    def __len__(self):
        return self.len

    def add(self, elem):
        if elem < 0:
            raise ValueError('UintSet elements must be >= 0')
        if elem in self:
            return
        word, bit = elem // 64, elem % 64
        while word >= len(self.words):
            self.words.append(0)
        self.words[word] |= 1 << bit
        self.len += 1

    def __contains__(self, elem):
        word, bit = elem // 64, elem % 64
        return (word < len(self.words) and
                (self.words[word] >> bit) & 1 == 1)

    def __iter__(self):
        for i, word in enumerate(self.words):
            if word == 0:
                continue
            for j in range(64):
                if word & (1 << j) != 0:
                    yield 64 * i+j

    def __repr__(self):
        parts = [self.__class__.__name__, '(']
        if self:
            parts.append('{')
            parts.append(', '.join(str(n) for n in self))
            parts.append('}')
        parts.append(')')
        return ''.join(parts)
