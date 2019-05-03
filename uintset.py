import bitops


INVALID_ELEMENT_MSG = "'UintSet' elements must be integers >= 0"
INVALID_ITER_ARG_MSG = "expected UintSet or iterable argument"
NOT_IN_SET_MSG = "element not in UintSet"
POP_EMPTY_MSG = "pop from an empty set"


class UintSet:

    def __init__(self, elements=None, bits=0):
        self._bits = bits
        if elements:
            for e in elements:
                self.add(e)

    def __len__(self):
        return bitops.count_ones(self._bits)

    def copy(self):
        return UintSet(bits=self._bits)

    def add(self, elem):
        try:
            self._bits = bitops.set_bit(self._bits, elem)
        except TypeError:
            raise TypeError(INVALID_ELEMENT_MSG)
        except ValueError:
            raise ValueError(INVALID_ELEMENT_MSG)

    def __contains__(self, elem):
        try:
            return bitops.get_bit(self._bits, elem)
        except TypeError:
            raise TypeError(INVALID_ELEMENT_MSG)
        except ValueError:
            raise ValueError(INVALID_ELEMENT_MSG)

    def __iter__(self):
        return bitops.find_ones(self._bits)

    def __repr__(self):
        elements = ', '.join(str(e) for e in self)
        if elements:
            elements = '{' + elements + '}'
        return f'UintSet({elements})'

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self._bits == other._bits

    def __or__(self, other):
        cls = self.__class__
        if isinstance(other, cls):
            res = cls()
            res._bits = self._bits | other._bits
            return res
        return NotImplemented

    def union(self, *others):
        cls = self.__class__
        res = cls()
        res._bits = self._bits
        for other in others:    
            if isinstance(other, cls):
                res._bits |= other._bits
            else:
                try:
                    second = cls(other)
                except TypeError:
                    raise TypeError(INVALID_ITER_ARG_MSG)
                else:
                    res._bits |= second._bits
        return res

    def __and__(self, other):
        cls = self.__class__
        if isinstance(other, cls):
            res = cls()
            res._bits = self._bits & other._bits
            return res
        return NotImplemented

    def intersection(self, *others):
        cls = self.__class__
        res = cls()
        res._bits = self._bits
        for other in others:    
            if isinstance(other, cls):
                res._bits &= other._bits
            try:
                second = cls(other)
            except TypeError:
                raise TypeError(INVALID_ITER_ARG_MSG)
            else:
                res._bits &= second._bits
        return res

    def __xor__(self, other):
        cls = self.__class__
        if isinstance(other, cls):
            res = cls()
            res._bits = self._bits ^ other._bits
            return res
        return NotImplemented

    def symmetric_difference(self, other):
        return self ^ other

    def __sub__(self, other):
        cls = self.__class__
        if isinstance(other, cls):
            res = self.copy()
            res._bits ^= self._bits & other._bits
            return res
        return NotImplemented
       
    def difference(self, *others):
        cls = self.__class__
        res = cls()
        res._bits = self._bits
        for other in others:    
            if isinstance(other, cls):
                res._bits ^= self._bits & other._bits
            else:
                try:
                    second = cls(other)
                except TypeError:
                    raise TypeError(INVALID_ITER_ARG_MSG)
                else:
                    res._bits ^= self._bits & second._bits
        return res

    def remove(self, elem):
        try:
            if elem not in self:
                raise KeyError(elem)
            self._bits = bitops.unset_bit(self._bits, elem)
        except TypeError:
            raise TypeError(INVALID_ELEMENT_MSG)
        except ValueError:
            raise ValueError(INVALID_ELEMENT_MSG)

    def pop(self):
        if self._bits == 0:
            raise KeyError(POP_EMPTY_MSG)
        elem = next(iter(self))
        self.remove(elem)
        return elem
       