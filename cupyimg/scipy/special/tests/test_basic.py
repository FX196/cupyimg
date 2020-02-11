import itertools
import unittest

import cupy
import numpy
from cupy import testing
import scipy.special  # NOQA

import cupyimg.scipy.special  # NOQA
from cupyimg.testing import numpy_cupyimg_allclose


@testing.gpu
@testing.with_requires("scipy")
class TestSpecialConvex(unittest.TestCase):
    def test_huber_basic(self):
        huber = cupyimg.scipy.special.huber
        assert huber(-1, 1.5) == cupy.inf
        testing.assert_allclose(huber(2, 1.5), 0.5 * 1.5 ** 2)
        testing.assert_allclose(huber(2, 2.5), 2 * (2.5 - 0.5 * 2))

    @testing.for_dtypes(["e", "f", "d"])
    @numpy_cupyimg_allclose(scipy_name="scp")
    def test_huber(self, xp, scp, dtype):
        z = testing.shaped_random((10, 2), xp=xp, dtype=dtype)
        return scp.special.huber(z[:, 0], z[:, 1])

    @testing.for_dtypes(["e", "f", "d"])
    @numpy_cupyimg_allclose(scipy_name="scp")
    def test_entr(self, xp, scp, dtype):
        values = (0, 0.5, 1.0, cupy.inf)
        signs = [-1, 1]
        arr = []
        for sgn, v in itertools.product(signs, values):
            arr.append(sgn * v)
        z = xp.asarray(arr, dtype=dtype)
        return scp.special.entr(z)

    @testing.for_dtypes(["e", "f", "d"])
    @numpy_cupyimg_allclose(scipy_name="scp")
    def test_rel_entr(self, xp, scp, dtype):
        values = (0, 0.5, 1.0)
        signs = [-1, 1]
        arr = []
        arr = []
        for sgna, va, sgnb, vb in itertools.product(
            signs, values, signs, values
        ):
            arr.append((sgna * va, sgnb * vb))
        z = xp.asarray(numpy.array(arr, dtype=dtype))
        return scp.special.kl_div(z[:, 0], z[:, 1])

    @testing.for_dtypes(["e", "f", "d"])
    @numpy_cupyimg_allclose(scipy_name="scp")
    def test_pseudo_huber(self, xp, scp, dtype):
        z = testing.shaped_random((10, 2), xp=numpy, dtype=dtype).tolist()
        z = xp.asarray(z + [[0, 0.5], [0.5, 0]], dtype=dtype)
        return scp.special.pseudo_huber(z[:, 0], z[:, 1])
