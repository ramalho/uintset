import array
import copy

WORD_SIZE = 64
ARRAY_TYPECODE = 'Q'  # unsigned long long -> 8 bytes
INVERT_MASK = 2 ** WORD_SIZE - 1


class UintSet():

    def __init__(self, it=None):
        self._words = array.array(ARRAY_TYPECODE)
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
        word, bit = elem // WORD_SIZE, elem % WORD_SIZE
        while word >= len(self._words):
            self._words.append(0)
        self._words[word] |= (1 << bit)
        self._len += 1

    def __contains__(self, elem):
        word, bit = elem // WORD_SIZE, elem % WORD_SIZE
        return (word < len(self._words) and
                (self._words[word] >> bit) & 1 == 1)

    def __iter__(self):
        for i, word in enumerate(self._words):
            if word == 0:
                continue
            for j in range(WORD_SIZE):
                if word & (1 << j):
                    yield WORD_SIZE * i+j

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

    def __or__(self, other):
        shorter, longer = short_long(self, other)
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

    def union(self, other):
        return self | other

    def __and__(self, other):
        shorter, longer = short_long(self, other)
        new = shorter.copy()
        n_words, l_words = new._words, longer._words
        for i in range(len(n_words)):
            n_word, l_word = n_words[i], l_words[i]
            if n_word != l_word:
                before = bit_count(n_word)
                n_word &= l_word
                new._len += bit_count(n_word) - before
                n_words[i] = n_word
        trim(new._words)
        return new

    def intersection(self, other):
        return self & other

    def __xor__(self, other):
        shorter, longer = short_long(self, other)
        new = longer.copy()
        n_words, s_words = new._words, shorter._words
        for i in range(len(s_words)):
            n_word, s_word = n_words[i], s_words[i]
            before = bit_count(n_word)
            n_word ^= s_word
            new._len += bit_count(n_word) - before
            n_words[i] = n_word
        trim(new._words)
        return new

    def symmetric_difference(self, other):
        return self ^ other

    def __sub__(self, other):
        new = self.copy()
        n_words, s_words, o_words = new._words, self._words, other._words
        for i in range(min(len(self._words), len(other._words))):
            n_word, s_word, o_word = n_words[i], s_words[i], o_words[i]
            before = bit_count(n_word)
            n_word ^= o_word & s_word
            new._len += bit_count(n_word) - before
            new._words[i] = n_word
        trim(new._words)
        return new

    def difference(self, other):
        return self - other

    def remove(self, elem):
        word, bit = elem // WORD_SIZE, elem % WORD_SIZE
        if (word < len(self._words) and
            (self._words[word] >> bit) & 1 == 1):
            self._words[word] &= (1 << bit) ^ INVERT_MASK
            self._len -= 1
            trim(self._words)


def short_long(a, b):
    if len(a) < len(b):
        return a, b
    return b, a


def bit_count(n):
    count = 0
    while n:
        count += n & 1
        n >>= 1
    return count


def trim(arr):
    while arr and arr[-1] == 0:
        del arr[-1]
