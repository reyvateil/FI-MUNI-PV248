import numpy as np

def calc(*args):
    dim = len(args) - 1
    np_array = np.asarray(args)

    try:
        np_vectors = np_array[1:] - np_array[0]
        np_vectors_trans = np.transpose(np_vectors)
        np_determinant = np.abs(np.linalg.det(np_vectors_trans))
    except (np.linalg.LinAlgError, TypeError):
        raise ValueError

    return np_determinant / np.math.factorial(dim)


from unittest import TestCase
class TestClass(TestCase):
    def test_2D_1(self):
        np.testing.assert_equal(calc((0,0), (3,4), (5,6)), 1)

    def test_2D_2(self):
        np.testing.assert_almost_equal(calc((3,3),(8,5),(1,12)),24.50,decimal=2)

    def test_3D_1(self):
        np.testing.assert_almost_equal(calc((0,0,0),(2,2,2),(3,3,0),(8,5,4)) , 3, decimal=2)

    def test_3D_2(self):
        np.testing.assert_almost_equal(calc((0,0,0),(2,0,0),(2,2,0),(2,2,2)), 1.33, decimal=2)

    def test_3D_3(self):
        np.testing.assert_almost_equal(calc((0,0,0),(3,0,0),(3,3,0),(3,3,3)), 4.5, decimal=2)

    def test_3D_4(self):
        np.testing.assert_almost_equal(calc((1,2,3),(1,0,0),(2,2,2),(3,5,6)), 0.17, decimal=2)

    def test_more_coords(self):
        self.assertRaises(ValueError, calc, (1,2),(2,3),(4,5),(8,3))

    def test_less_coords(self):
        self.assertRaises(ValueError, calc, (1,2),(2,3))

    def test_inconsistent_coords(self):
        self.assertRaises(ValueError, calc, (1,2),(2,3,4),(4,5))

    def test_inconsistend_and_more_coords(self):
        self.assertRaises(ValueError, calc, (1,2),(2,3,4),(4,5),(8,3))