import os

from cffi import FFI


SRC_ROOT = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'croaring-src')

FFI_BUILDER = FFI()

# The following header code was adapted from the CRoaring amalgamated header,
# which is released under the Apache License v2.0. See the LICENSING file for
# details.
FFI_BUILDER.cdef('''
typedef struct roaring_bitmap_s {
    ...;
} roaring_bitmap_t;

roaring_bitmap_t *roaring_bitmap_create(void);
roaring_bitmap_t *roaring_bitmap_from_range(uint32_t min, uint32_t max,
                                            uint32_t step);
roaring_bitmap_t *roaring_bitmap_copy(const roaring_bitmap_t *r);

roaring_bitmap_t *roaring_bitmap_and(const roaring_bitmap_t *x1,
                                     const roaring_bitmap_t *x2);
void roaring_bitmap_and_inplace(roaring_bitmap_t *x1,
                                const roaring_bitmap_t *x2);
uint64_t roaring_bitmap_and_cardinality(const roaring_bitmap_t *x1,
                                        const roaring_bitmap_t *x2);
bool roaring_bitmap_intersect(const roaring_bitmap_t *x1,
                              const roaring_bitmap_t *x2);

roaring_bitmap_t *roaring_bitmap_or(const roaring_bitmap_t *x1,
                                    const roaring_bitmap_t *x2);
void roaring_bitmap_or_inplace(roaring_bitmap_t *x1,
                               const roaring_bitmap_t *x2);
uint64_t roaring_bitmap_or_cardinality(const roaring_bitmap_t *x1,
                                       const roaring_bitmap_t *x2);

roaring_bitmap_t *roaring_bitmap_xor(const roaring_bitmap_t *x1,
                                     const roaring_bitmap_t *x2);
void roaring_bitmap_xor_inplace(roaring_bitmap_t *x1,
                                const roaring_bitmap_t *x2);
uint64_t roaring_bitmap_xor_cardinality(const roaring_bitmap_t *x1,
                                        const roaring_bitmap_t *x2);

roaring_bitmap_t *roaring_bitmap_andnot(const roaring_bitmap_t *x1,
                                        const roaring_bitmap_t *x2);
void roaring_bitmap_andnot_inplace(roaring_bitmap_t *x1,
                                   const roaring_bitmap_t *x2);
uint64_t roaring_bitmap_andnot_cardinality(const roaring_bitmap_t *x1,
                                           const roaring_bitmap_t *x2);

void roaring_bitmap_free(roaring_bitmap_t *r);
void roaring_bitmap_add(roaring_bitmap_t *r, uint32_t x);
void roaring_bitmap_remove(roaring_bitmap_t *r, uint32_t x);
void roaring_bitmap_clear(roaring_bitmap_t *ra);
bool roaring_bitmap_contains(const roaring_bitmap_t *r,
                                           uint32_t val);
uint64_t roaring_bitmap_get_cardinality(const roaring_bitmap_t *ra);
bool roaring_bitmap_is_empty(const roaring_bitmap_t *ra);
bool roaring_bitmap_equals(const roaring_bitmap_t *ra1, const roaring_bitmap_t *ra2);
bool roaring_bitmap_is_subset(const roaring_bitmap_t *ra1, const roaring_bitmap_t *ra2);

bool roaring_bitmap_run_optimize(roaring_bitmap_t *r);
size_t roaring_bitmap_shrink_to_fit(roaring_bitmap_t *r);

size_t roaring_bitmap_portable_size_in_bytes(const roaring_bitmap_t *ra);
size_t roaring_bitmap_portable_serialize(const roaring_bitmap_t *ra, char *buf);
roaring_bitmap_t *roaring_bitmap_portable_deserialize(const char *buf);

bool roaring_bitmap_select(const roaring_bitmap_t *ra, uint32_t rank,
                           uint32_t *element);
uint64_t  roaring_bitmap_rank(const roaring_bitmap_t *bm, uint32_t x);

uint32_t roaring_bitmap_minimum(const roaring_bitmap_t *bm);
uint32_t roaring_bitmap_maximum(const roaring_bitmap_t *bm);

typedef struct roaring_statistics_s {
    uint32_t n_containers; /* number of containers */

    uint32_t n_array_containers;  /* number of array containers */
    uint32_t n_run_containers;    /* number of run containers */
    uint32_t n_bitset_containers; /* number of bitmap containers */

    uint32_t
        n_values_array_containers;    /* number of values in array containers */
    uint32_t n_values_run_containers; /* number of values in run containers */
    uint32_t
        n_values_bitset_containers; /* number of values in  bitmap containers */

    uint32_t n_bytes_array_containers;  /* number of allocated bytes in array
                                           containers */
    uint32_t n_bytes_run_containers;    /* number of allocated bytes in run
                                           containers */
    uint32_t n_bytes_bitset_containers; /* number of allocated bytes in  bitmap
                                           containers */

    uint32_t
        max_value; /* the maximal value, undefined if cardinality is zero */
    uint32_t
        min_value; /* the minimal value, undefined if cardinality is zero */
    uint64_t sum_value; /* the sum of all values (could be used to compute
                           average) */

    uint64_t cardinality; /* total number of values stored in the bitmap */

    // and n_values_arrays, n_values_rle, n_values_bitmap
} roaring_statistics_t;

void roaring_bitmap_statistics(const roaring_bitmap_t *ra,
                               roaring_statistics_t *stat);


typedef struct roaring_uint32_iterator_s {
  const roaring_bitmap_t *parent; // owner
  ...;
  uint32_t current_value;
  bool has_value;
} roaring_uint32_iterator_t;
roaring_uint32_iterator_t * roaring_create_iterator(const roaring_bitmap_t *ra);
bool roaring_advance_uint32_iterator(roaring_uint32_iterator_t *it);
roaring_uint32_iterator_t * roaring_copy_uint32_iterator(const roaring_uint32_iterator_t * it);
void roaring_free_uint32_iterator(roaring_uint32_iterator_t *it);
''')

FFI_BUILDER.set_source(
    'croaring._roaring',
    '#include "roaring.c"',
    include_dirs=[SRC_ROOT],
    extra_compile_args=['-std=c11', '-msse4.2'])

if __name__ == '__main__':
    FFI_BUILDER.compile(verbose=True)
