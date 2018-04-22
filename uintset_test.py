import pytest

from uintset import UintSet


def test_new():
    s = UintSet()
    assert len(s) == 0


def test_new_from_iterable():
    s = UintSet([1, 2, 3])
    assert len(s) == 3


def test_add():
    s = UintSet()
    s.add(1)
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
