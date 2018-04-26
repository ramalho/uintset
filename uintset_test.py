import collections
import pytest
import array

from uintset import UintSet, bit_count, trim


def test_new():
    s = UintSet()
    assert len(s) == 0


def test_new_from_iterable():
    s = UintSet([1, 100, 3])  # beyond word 0
    assert len(s) == 3


def test_add():
    s = UintSet()
    s.add(0)
    assert len(s) == 1


def test_add_multiple():
    s = UintSet()
    s.add(1)
    s.add(3)
    s.add(1)
    assert len(s) == 2


def test_add_negative():
    s = UintSet()
    with pytest.raises(ValueError):
        s.add(-1)


def test_contains():
    s = UintSet()
    s.add(1)
    assert 1 in s


def test_iter():
    s = UintSet([1, 5, 0, 3, 2, 4])
    assert list(s) == [0, 1, 2, 3, 4, 5]


def test_repr_empty():
    s = UintSet()
    assert repr(s) == 'UintSet()'


def test_repr():
    s = UintSet([1, 5, 0, 3, 2, 4])
    assert repr(s) == 'UintSet({0, 1, 2, 3, 4, 5})'


def test_eq():
    TC = collections.namedtuple('TestCase', 's1 s2 want')
    test_cases = [
        TC(UintSet(), UintSet(), True),
        TC(UintSet([1]), UintSet(), False),
        TC(UintSet(), UintSet([1]), False),
        TC(UintSet([1, 2, 100]), UintSet([100, 2, 1]), True), # beyond word 0
        TC(UintSet([1, 100]), UintSet([1, 101]), False),
        TC(UintSet([1, 100]), UintSet([1, 100, 1000]), False),
    ]
    for t in test_cases:
        assert (t.s1 == t.s2) is t.want


def test_copy():
    test_cases = [
        UintSet(),
        UintSet([1]),
        UintSet([1, 2]),
        UintSet([1, 100]),  # beyond word 0
    ]
    for s1 in test_cases:
        s2 = s1.copy()
        assert s1 == s2


def test_bit_count():
    test_cases = [
        (0, 0),
        (1, 1),
        (2, 1),
        (3, 2),
        (4, 1),
        (10, 2),
        (11, 3),
        (63, 6),
        (64, 1),
        (2 ** 64-2, 63),
        (2 ** 64-1, 64),
        (2 ** 64, 1),
    ]
    for n, want in test_cases:
        assert bit_count(n) == want


def test_union():
    TC = collections.namedtuple('TestCase', 's1 s2 want')
    test_cases = [
        TC(UintSet(), UintSet(), UintSet()),
        TC(UintSet([1]), UintSet(), UintSet([1])),
        TC(UintSet(), UintSet([1]), UintSet([1])),
        TC(UintSet([1, 100]), UintSet([100, 1]), UintSet([100, 1])), # beyond word 0
        TC(UintSet([1, 100]), UintSet([2]), UintSet([1, 2, 100])),
    ]
    for t in test_cases:
        got = t.s1.union(t.s2)
        assert len(got) == len(t.want)
        assert got == t.want


def test_intersection():
    test_cases = [
        (UintSet(), UintSet(), UintSet()),
        (UintSet([1]), UintSet(), UintSet()),
        (UintSet([1]), UintSet([1]), UintSet([1])),
        (UintSet([1, 100]), UintSet([100, 1]), UintSet([100, 1])), # beyond word 0
        (UintSet([1, 100]), UintSet([2]), UintSet()),
        (UintSet([1, 2, 3, 4]), UintSet([2, 3, 5]), UintSet([2, 3])),
    ]
    for s1, s2, want in test_cases:
        got = s1.intersection(s2)
        assert len(got) == len(want)
        assert got == want


def test_symmetric_difference():
    test_cases = [
        (UintSet(), UintSet(), UintSet()),
        (UintSet([1]), UintSet(), UintSet([1])),
        (UintSet([1]), UintSet([1]), UintSet()),
        (UintSet([1, 100]), UintSet([100, 1]), UintSet()), # beyond word 0
        (UintSet([1, 100]), UintSet([2]), UintSet([1, 100, 2])),
        (UintSet([1, 2, 3, 4]), UintSet([2, 3, 5]), UintSet([1, 4, 5])),
    ]
    for s1, s2, want in test_cases:
        got = s1.symmetric_difference(s2)
        assert len(got) == len(want)
        assert got == want


def test_difference():
    test_cases = [
        (UintSet(), UintSet(), UintSet()),
        (UintSet([1]), UintSet(), UintSet([1])),
        (UintSet([1]), UintSet([1]), UintSet()),
        (UintSet([1, 100]), UintSet([100, 1]), UintSet()), # beyond word 0
        (UintSet([1, 100]), UintSet([2]), UintSet([1, 100])),
        (UintSet([1, 2, 3, 4]), UintSet([2, 3, 5]), UintSet([1, 4])),
    ]
    for s1, s2, want in test_cases:
        got = s1.difference(s2)
        assert len(got) == len(want)
        assert got == want


def test_trim_array():
    test_cases = [
        (array.array('L', []), array.array('L', [])),
        (array.array('L', [0]), array.array('L', [])),
        (array.array('L', [1, 0]), array.array('L', [1])),
        (array.array('L', [0, 1]), array.array('L', [0, 1])),
    ]
    for a, want in test_cases:
        trim(a)
        assert a == want


def test_remove():
    test_cases = [
        (UintSet(), 1, UintSet()),
        (UintSet([0]), 0, UintSet()),
        (UintSet([1, 2, 3]), 2, UintSet([1, 3])),
        (UintSet([1, 2, 3]), 9, UintSet([1, 2, 3])),
    ]
    for s, elem, want in test_cases:
        s.remove(elem)
        assert s == want
