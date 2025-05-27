# guavahash

[![Build](https://github.com/igorcoding/guavahash/actions/workflows/ci.yaml/badge.svg?branch=refresh)](https://github.com/igorcoding/guavahash/actions)
[![PyPI](https://img.shields.io/pypi/v/guavahash.svg)](https://pypi.python.org/pypi/guavahash
)

Google's Guava consistent hashing implementation


Assign to `input` a "bucket" in the range `[0, buckets)`, in a uniform manner
that minimizes the need for remapping as `buckets` grows.
That is, `consistentHash(h, n)` equals:

* `n - 1`, with approximate probability `1/n`;
* `consistentHash(h, n - 1)`, otherwise (probability `1 - 1/n`).

See the [wikipedia article on consistent hashing](http://en.wikipedia.org/wiki/Consistent_hashing)
for more information.
