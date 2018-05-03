import array
import copy

WORD_SIZE = 64
# typecodes: 'L' -> 32 bits, 'Q' -> 64 bits
ARRAY_TYPECODE = 'Q'
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
                get_bit(self._words[word], bit))

    def __iter__(self):
        for word, bitmap in enumerate(self._words):
            if bitmap == 0:
                continue
            for bit in range(WORD_SIZE):
                if get_bit(bitmap, bit):
                    yield WORD_SIZE * word + bit

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

    def union(self, *others):
        new_set = self.copy()
        for other in others:
            if not hasattr(other, '_words'):
                other = UintSet(other)
            new_set = new_set | other  # TODO: compute this in-place
        return new_set

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
        s_words = self._words
        if (word < len(s_words) and
            get_bit(s_words[word], bit)):
            s_words[word] = unset_bit(s_words[word], bit)
            self._len -= 1
            trim(s_words)
        else:
            raise KeyError(elem)

    def pop(self):
        if not self:
            raise KeyError('pop from an empty set')

        bitmap = self._words[-1]
        word = WORD_SIZE * (len(self._words) - 1)
        bit = WORD_SIZE - 1
        while bit >= 0:
            if get_bit(bitmap, bit):
                break
            bit -= 1
        else:
            assert False, 'Should never get here'

        elem = word + bit
        self._words[-1] = unset_bit(bitmap, bit)
        self._len -= 1
        trim(self._words)
        return elem


def short_long(a, b):
    if len(a) < len(b):
        return a, b
    return b, a


def bit_count(bitmap):
    count = 0
    while bitmap:
        count += bitmap & 1
        bitmap >>= 1
    return count


def trim(arr):
    while arr and arr[-1] == 0:
        del arr[-1]


def get_bit(bitmap, bit):
    return (bitmap >> bit) & 1


def unset_bit(bitmap, bit):
    return bitmap & ((1 << bit) ^ INVERT_MASK)
