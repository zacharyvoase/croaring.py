import operator
import random
import six

from nose.tools import assert_equals
from nose.tools import assert_raises

from croaring import RoaringBitmap


EMPTY = set()


BINARY_OPERATORS = [
    (operator.and_, "&"),
    (operator.or_, "|"),
    (operator.xor, "^"),
    (operator.sub, "-"),
]


INPLACE_OPERATORS = [
    (operator.iand, "&="),
    (operator.ior, "|="),
    (operator.ixor, "^="),
    (operator.isub, "-="),
]


def gen_random_set_pairs():
    if six.PY2:
        range_ = xrange
    else:
        range_ = range

    initial = random.sample(range_(0, 1000), 50)
    equal = initial[:]
    disjoint = random.sample(range_(1000, 2000), 50)
    overlap = initial[:25] + random.sample(range_(1000, 2000), 25)
    proper_subset = initial[:25]
    proper_superset = initial + disjoint

    yield (EMPTY, EMPTY, "empty {} empty")
    yield (initial, EMPTY, "X {} empty")
    yield (initial, equal, "X {} X")
    yield (initial, disjoint, "X {} disjoint")
    yield (initial, overlap, "X {} overlap")
    yield (initial, proper_subset, "X {} proper_subset")
    yield (initial, proper_superset, "X {} proper_superset")


def test_range():
    yield check_range_same, 0, 10
    yield check_range_same, 0, 10, 1
    yield check_range_same, 0, 10, 2
    yield check_range_same, 0, 10, 3


def test_binary_operators():
    for op, op_name in BINARY_OPERATORS:
        for (s1, s2, name) in gen_random_set_pairs():
            yield check_binary_same, op, s1, s2, name.format(op_name)


def test_inplace_operators():
    for op, op_name in INPLACE_OPERATORS:
        for (s1, s2, name) in gen_random_set_pairs():
            yield check_inplace_same, op, s1, s2, name.format(op_name)


def check_range_same(*range_args):
    range_ = six.PY2 and range or (lambda *a: list(range(*a)))
    assert_equals(list(RoaringBitmap.range(*range_args)), range_(*range_args))


def check_binary_same(op, set1, set2, name):
    expected = list(op(set(set1), set(set2)))
    expected.sort()
    actual = list(op(RoaringBitmap(set1), RoaringBitmap(set2)))
    assert_equals(actual, expected, name)
    with assert_raises(TypeError):
        op(RoaringBitmap(set1), set(set2))


def check_inplace_same(op, set1, set2, name):
    s1, s2 = set(set1), set(set2)
    bm1, bm2 = RoaringBitmap(set1), RoaringBitmap(set2)
    op(s1, s2)
    op(bm1, bm2)
    expected = list(s1)
    expected.sort()
    actual = list(bm1)
    assert_equals(actual, expected, name)
    with assert_raises(TypeError):
        op(bm1, s2)
