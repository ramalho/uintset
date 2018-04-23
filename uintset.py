import array
import copy

class UintSet():

    def __init__(self, it=None):
        self._words = array.array('L')
        self._len = 0
        if it is not None:
            for i in it:
                self.add(i)

    def __len__(self):
        return self._len

    def add(self, elem):
        if elem < 0:
            raise ValueError('UintSet elements must be >= 0')
        if elem in self:
            return
        word, bit = elem // 64, elem % 64
        while word >= len(self._words):
            self._words.append(0)
        self._words[word] |= (1 << bit)
        self._len += 1

    def __contains__(self, elem):
        word, bit = elem // 64, elem % 64
        return (word < len(self._words) and
                (self._words[word] >> bit) & 1 == 1)

    def __iter__(self):
        for i, word in enumerate(self._words):
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

    def __eq__(self, other):
        return (len(self) == len(other)
                and self._words == other._words)

    def copy(self):
        clone = UintSet()
        clone._words = copy.copy(self._words)
        clone._len = self._len
        return clone

    def union(self, other):
        if len(self) > len(other):
            longer = self
            shorter = other
        else:
            longer = other
            shorter = self
        new = longer.copy()
        n_words, s_words = new._words, shorter._words
        for i in range(len(s_words)):
            n_word, s_word = n_words[i], s_words[i]
            if n_word != s_word:
                before = bit_count(n_word)
                n_word |= s_word
                new._len += bit_count(n_word) - before
                n_words[i] = n_word
        return new

    def intersection(self, other):
        if len(self) > len(other):
            longer = self
            shorter = other
        else:
            longer = other
            shorter = self
        new = shorter.copy()
        n_words, l_words = new._words, longer._words
        for i in range(len(n_words)):
            n_word, l_word = n_words[i], l_words[i]
            if n_word != l_word:
                before = bit_count(n_word)
                n_word &= l_word
                new._len += bit_count(n_word) - before
                n_words[i] = n_word
        # trim zero-only words at end of array
        while new._words and new._words[-1] == 0:
            del new._words[-1]
        return new

    def symmetric_difference(self, other):
        if len(self) > len(other):
            longer = self
            shorter = other
        else:
            longer = other
            shorter = self
        new = longer.copy()
        n_words, s_words = new._words, shorter._words
        for i in range(len(s_words)):
            n_word, s_word = n_words[i], s_words[i]
            before = bit_count(n_word)
            n_word ^= s_word
            new._len += bit_count(n_word) - before
            n_words[i] = n_word
        # trim zero-only words at end of array
        while new._words and new._words[-1] == 0:
            del new._words[-1]
        return new

    def difference(self, other):
        new = self.copy()
        for i in range(min(len(self._words), len(other._words))):
            n_word, s_word, o_word = new._words[i], self._words[i], other._words[i]
            before = bit_count(n_word)
            n_word ^= o_word & s_word
            new._len += bit_count(n_word) - before
            new._words[i] = n_word
        # trim zero-only words at end of array
        while new._words and new._words[-1] == 0:
            del new._words[-1]
        return new



def bit_count(n):
    count = 0
    while n:
        count += n & 1
        n >>= 1
    return count

