# uintset

A Python set type designed for dense sets of non-negative integers. Each element is represented as a `1` bit in the corresponding position within an array of 64-bit unsigned integers (words).

Membership test `n in s` is _O(1)_ because the bit that represents `n` in the `s` set is in word `n // 64`, at bit offset `n % 64`.

Adding an element means setting a bit at the corresponding word and offset, extending the array with more words if needed.

Set operations such as union, intersection, and symmetric difference are implemented using the bitwise operators `|`, `&`, and `^` on the array words.

> This package is inspired by the `intset` example in chapter 6 of
_The Go Programming Language_, by Donovan & Kernighan.
