import operator

from nose.tools import assert_raises
import six

from croaring import RoaringBitmap


def test_smoke():
    bm = RoaringBitmap()
    assert len(bm) == 0
    assert list(bm) == []
    assert not bm
    assert 1 not in bm

    printed = repr(bm)
    assert isinstance(printed, six.string_types)

    bm.add(1)
    bm.add(6)
    assert len(bm) == 2
    assert list(bm) == [1, 6]
    assert bm
    assert 1 in bm
    assert 6 in bm
    assert 2 not in bm

    bm.discard(1)
    assert len(bm) == 1
    assert list(bm) == [6]
    assert bm
    assert 1 not in bm
    assert 6 in bm


def test_invalid_args():
    with assert_raises(TypeError):
        RoaringBitmap(123)
    with assert_raises(TypeError):
        RoaringBitmap('string')


def test_minmax():
    empty = RoaringBitmap([])
    assert empty.minimum() is None
    assert empty.maximum() is None

    bm = RoaringBitmap([1, 2, 3, 4])
    assert bm.minimum() == 1
    assert bm.maximum() == 4


def test_indexing_empty():
    empty = RoaringBitmap([])
    with assert_raises(IndexError):
        empty[0]
    with assert_raises(IndexError):
        empty[-1]


def test_indexing_nonempty():
    bm = RoaringBitmap([1, 3, 5, 6])
    assert bm[0] == 1
    assert bm[1] == 3
    assert bm[2] == 5
    assert bm[3] == 6
    with assert_raises(IndexError):
        bm[4]
    assert bm[-1] == 6
    assert bm[-2] == 5
    assert bm[-3] == 3
    assert bm[-4] == 1
    with assert_raises(IndexError):
        bm[-5]


def test_copy():
    bm = RoaringBitmap()
    bm.add(1)
    bm2 = bm.copy()
    bm2.add(6)
    assert len(bm) == 1
    assert list(bm) == [1]
    assert len(bm2) == 2
    assert list(bm2) == [1, 6]


def test_isdisjoint():
    empty = RoaringBitmap()
    assert empty.isdisjoint(empty)
    bm1 = RoaringBitmap([1, 2, 3, 4, 5])
    bm2 = RoaringBitmap([6, 7, 8, 9, 10])
    bm3 = RoaringBitmap([4, 5, 6, 7])
    assert bm1.isdisjoint(empty)
    assert empty.isdisjoint(bm1)
    assert bm1.isdisjoint(bm2)
    assert not bm1.isdisjoint(bm3)
    assert not bm2.isdisjoint(bm3)
    assert not bm3.isdisjoint(bm1)
    assert not bm3.isdisjoint(bm2)


def test_clear():
    bm = RoaringBitmap([1, 2, 3, 4, 5])
    bm.clear()
    assert len(bm) == 0
    assert list(bm) == []
