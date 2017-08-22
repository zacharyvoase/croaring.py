import collections
import functools

import six

from croaring._roaring import ffi, lib


__all__ = ['RoaringBitmap']


def guard(func):
    """Decorator to ensure that both args to a method are RoaringBitmaps."""
    @functools.wraps(func)
    def guarded(self, other):
        if not isinstance(other, RoaringBitmap):
            raise TypeError("Expected RoaringBitmap, got {!r}".format(other))
        return func(self, other)
    return guarded


def bitmap_operator(lib_func):
    """Simple wrapper for binary bitmap operators."""
    @guard
    def operator(self, other):
        return RoaringBitmap(lib_func(self._bitmap, other._bitmap))
    return operator


def bitmap_assign_operator(lib_func):
    """Simple wrapper for binary in-place bitmap operators."""
    @guard
    def operator(self, other):
        lib_func(self._bitmap, other._bitmap)
        return self
    return operator


class RoaringBitmap(collections.MutableSet):

    """An efficient integer bitmap set, based on CRoaring."""

    @classmethod
    def range(cls, *args):
        """Build a RoaringBitmap with arguments similar to range()."""
        if len(args) == 1:
            start, stop, step = 0, args[0], 1
        elif len(args) == 2:
            start, stop, step = args[0], args[1], 1
        elif len(args) == 3:
            start, stop, step = args
        else:
            raise TypeError("RoaringBitmap.range() expects exactly 1, 2, or 3 arguments")

        if start < 0 or stop < 0 or step < 0:
            raise ValueError("all arguments to range() must be positive")
        if step == 0:
            raise ValueError("step argument to range() cannot be zero")

        return cls(lib.roaring_bitmap_from_range(start, stop, step))

    def __init__(self, bitmap=None):
        if isinstance(bitmap, ffi.CData) and ffi.typeof(bitmap).cname == 'struct roaring_bitmap_s *':
            self._bitmap = bitmap
        elif bitmap is None:
            self._bitmap = lib.roaring_bitmap_create()
        elif isinstance(bitmap, collections.Iterable):
            self._bitmap, iterable = lib.roaring_bitmap_create(), bitmap
            for value in iterable:
                self.add(value)
        else:
            raise TypeError("Can't initialize RoaringBitmap from {!r}".format(bitmap))

    def __repr__(self):
        return 'RoaringBitmap([{}])'.format(', '.join(repr(num) for num in self))

    def __bool__(self):
        return not bool(lib.roaring_bitmap_is_empty(self._bitmap))

    if six.PY2:
        __nonzero__ = __bool__
        del __bool__

    def __len__(self):
        return lib.roaring_bitmap_get_cardinality(self._bitmap)

    def __del__(self):
        lib.roaring_bitmap_free(self._bitmap)

    def __contains__(self, value):
        return bool(lib.roaring_bitmap_contains(self._bitmap, value))

    def __iter__(self):
        iterator = lib.roaring_create_iterator(self._bitmap)
        try:
            while iterator.has_value:
                yield iterator.current_value
                lib.roaring_advance_uint32_iterator(iterator)
        finally:
            lib.roaring_free_uint32_iterator(iterator)

    @guard
    def __eq__(self, other):
        return bool(lib.roaring_bitmap_equals(self._bitmap, other._bitmap))

    __and__ = bitmap_operator(lib.roaring_bitmap_and)
    __or__ = bitmap_operator(lib.roaring_bitmap_or)
    __xor__ = bitmap_operator(lib.roaring_bitmap_xor)
    __sub__ = bitmap_operator(lib.roaring_bitmap_andnot)

    __iand__ = bitmap_assign_operator(lib.roaring_bitmap_and_inplace)
    __ior__ = bitmap_assign_operator(lib.roaring_bitmap_or_inplace)
    __ixor__ = bitmap_assign_operator(lib.roaring_bitmap_xor_inplace)
    __isub__ = bitmap_assign_operator(lib.roaring_bitmap_andnot_inplace)

    @guard
    def __lt__(self, other):
        return len(self) < len(other) and self <= other

    @guard
    def __gt__(self, other):
        return other < self

    @guard
    def __le__(self, other):
        return bool(lib.roaring_bitmap_is_subset(self._bitmap, other._bitmap))

    @guard
    def __ge__(self, other):
        return other <= self

    def add(self, value):
        lib.roaring_bitmap_add(self._bitmap, value)

    def discard(self, value):
        lib.roaring_bitmap_remove(self._bitmap, value)

    def clear(self):
        lib.roaring_bitmap_clear(self._bitmap)

    union = __or__
    intersection = __and__
    difference = __sub__
    symmetric_difference = __xor__
    issubset = __le__
    issuperset = __ge__

    @guard
    def isdisjoint(self, other):
        return not lib.roaring_bitmap_intersect(self._bitmap, other._bitmap)

    def copy(self):
        return RoaringBitmap(lib.roaring_bitmap_copy(self._bitmap))

    def minimum(self):
        if not self:
            return None
        return lib.roaring_bitmap_minimum(self._bitmap)

    def maximum(self):
        if not self:
            return None
        return lib.roaring_bitmap_maximum(self._bitmap)

    def __getitem__(self, index):
        if not self:
            raise IndexError("RoaringBitmap index out of range")
        elif index == 0:
            return self.minimum()
        elif index == -1:
            return self.maximum()
        elif index < 0:
            if abs(index) <= len(self):
                return self[len(self) + index]
            raise IndexError("RoaringBitmap index out of range")
        elem = ffi.new('uint32_t *')
        found = lib.roaring_bitmap_select(self._bitmap, index, elem)
        if found:
            return elem[0]
        raise IndexError("RoaringBitmap index out of range")
