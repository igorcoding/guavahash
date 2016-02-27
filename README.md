# guavahash
[![Build Status](https://travis-ci.org/igorcoding/guavahash.svg?branch=master)](https://travis-ci.org/igorcoding/guavahash)

Google's Guava consistent hashing implementation


Assign to `input` a "bucket" in the range `[0, buckets)`, in a uniform manner
that minimizes the need for remapping as `buckets` grows.
That is, `consistentHash(h, n)` equals:

* `n - 1`, with approximate probability `1/n`;
* `consistentHash(h, n - 1)`, otherwise (probability `1 - 1/n`).

See the [wikipedia article on consistent hashing](http://en.wikipedia.org/wiki/Consistent_hashing)
for more information.
