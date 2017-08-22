# CRoaring.py: Fast, compact integer bitmap sets, based on CRoaring

[![Build Status](https://travis-ci.org/zacharyvoase/croaring.py.svg?branch=master)](https://travis-ci.org/zacharyvoase/croaring.py)
[![codecov](https://codecov.io/gh/zacharyvoase/croaring.py/branch/master/graph/badge.svg)](https://codecov.io/gh/zacharyvoase/croaring.py)

[Roaring bitmaps][] are fast, compressed, and portable bitmaps, used to store
unique sorted integer sets. These bitmaps offer better real-world space
complexity and performance than typical hash sets (such as Python's built-in
`set`), and can be serialized into a portable format for storage and interop
with the C/C++, Java and Go libraries.

This library makes the [CRoaring][] implementation available in Python 2.7 and
3.5+. It uses [CFFI][], so it works on both CPython and PyPy. The full Python
`set` interface is implemented. Comprehensive tests are included.

  [Roaring bitmaps]: http://roaringbitmap.org/
  [CRoaring]: https://github.com/RoaringBitmap/CRoaring
  [CFFI]: http://cffi.readthedocs.io/en/latest/


## Installation

    pip install croaring

The CRoaring source is included with the Python library, so you don't need to
install it from elsewhere (though you may need a C compiler available if a
binary package is unavailable for your architecture).


## Usage

Instantiate a `croaring.RoaringBitmap()`, and use it just like a normal `set`:

    >>> import croaring
    >>> bitmap = croaring.RoaringBitmap()
    >>> bitmap
    RoaringBitmap([])
    >>> bitmap.add(1)
    >>> bitmap.add(4572)
    >>> bitmap.add(326)
    >>> bitmap
    RoaringBitmap([1, 326, 4572])

You can use either binary operators (`|`, `&`, `^` and `-`) or their English
names (`union`, `intersection`, `symmetric_difference` and `difference`):

    >>> bitmap | RoaringBitmap([50, 95])
    RoaringBitmap([1, 50, 95, 326, 4572])
    >>> bitmap & RoaringBitmap([200, 326])
    RoaringBitmap([326])
    >>> bitmap ^ RoaringBitmap([200, 326])
    RoaringBitmap([1, 200, 4572])

Since the bitmaps are ordered, indexing (including negative) is supported:

    >>> bitmap[1]
    326
    >>> bitmap[-1]
    4572

Finally, you can construct a bitmap from a range, similar to the arguments to
Python's built-in `range`:

    >>> RoaringBitmap.range(10)
    RoaringBitmap([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    >>> RoaringBitmap.range(2, 10)
    RoaringBitmap([2, 3, 4, 5, 6, 7, 8, 9])
    >>> RoaringBitmap.range(2, 10, 3)
    RoaringBitmap([2, 5, 8])


## License

CRoaring is licensed under the Apache License v2.0:

> Copyright 2016 The CRoaring authors
>
> Licensed under the Apache License, Version 2.0 (the "License");
> you may not use this file except in compliance with the License.
> You may obtain a copy of the License at
>
>     http://www.apache.org/licenses/LICENSE-2.0
>
> Unless required by applicable law or agreed to in writing, software
> distributed under the License is distributed on an "AS IS" BASIS,
> WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
> See the License for the specific language governing permissions and
> limitations under the License.

All other code is released under the Unlicense:

> This is free and unencumbered software released into the public domain.
>
> Anyone is free to copy, modify, publish, use, compile, sell, or
> distribute this software, either in source code form or as a compiled
> binary, for any purpose, commercial or non-commercial, and by any
> means.
>
> In jurisdictions that recognize copyright laws, the author or authors
> of this software dedicate any and all copyright interest in the
> software to the public domain. We make this dedication for the benefit
> of the public at large and to the detriment of our heirs and
> successors. We intend this dedication to be an overt act of
> relinquishment in perpetuity of all present and future rights to this
> software under copyright law.
>
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
> EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
> MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
> IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
> OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
> ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
> OTHER DEALINGS IN THE SOFTWARE.
>
> For more information, please refer to <http://unlicense.org/>
