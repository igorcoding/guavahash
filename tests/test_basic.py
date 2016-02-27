import unittest
import json
import os
import guavahash

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class TestCase(unittest.TestCase):
    def test_basic(self):
        with open(os.path.join(BASE_DIR, 'testdata.json'), 'r') as f:
            testdata = f.read()
        case_arr = json.loads(testdata)

        for case in case_arr:
            state, n_buckets, expected = tuple(case)
            guava_res = guavahash.guava(state, n_buckets)

            message = "({0}, {1}) => {2} vs {3}".format(state, n_buckets, expected, guava_res)
            self.assertEqual(guava_res, expected, message)
