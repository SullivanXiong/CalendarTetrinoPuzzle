import unittest

from calender_solver.calender_solver.tetrino import (InvalidShapeError, Shape,
                                                     Tetrino)


class TestTetrino(unittest.TestCase):
    def setUp(self):
        """
        Set up test data for Tetrino pieces.
        """
        self.small_L_tetrino = Tetrino(Shape(2, 3, [[1, 0], [1, 0], [1, 1]]), "sL")

    def test_initial_shape(self):
        """
        Test the initial shape of the Tetrino.
        """
        expected_shape = [[1, 0], [1, 0], [1, 1]]
        self.assertEqual(self.small_L_tetrino.shape.shape, expected_shape)

    def test_rotate_90(self):
        """
        Test rotating the Tetrino 90 degrees clockwise.
        """
        self.small_L_tetrino.rotate_clockwise(90)
        expected_shape = [[1, 1, 1], [1, 0, 0]]
        self.assertEqual(self.small_L_tetrino.shape.shape, expected_shape)

    def test_rotate_180(self):
        """
        Test rotating the Tetrino 180 degrees clockwise.
        """
        self.small_L_tetrino.rotate_clockwise(180)
        expected_shape = [[1, 1], [0, 1], [0, 1]]
        self.assertEqual(self.small_L_tetrino.shape.shape, expected_shape)

    def test_rotate_360(self):
        """
        Test rotating the Tetrino 360 degrees clockwise (full rotation).
        """
        self.small_L_tetrino.rotate_clockwise(360)
        expected_shape = [[1, 0], [1, 0], [1, 1]]  # Should return to the original shape
        self.assertEqual(self.small_L_tetrino.shape.shape, expected_shape)

    def test_invalid_shape(self):
        """
        Test that an invalid shape raises an InvalidShapeError.
        """
        with self.assertRaises(InvalidShapeError):
            Tetrino(Shape(2, 3, [[1, 0], [1, 0]]), "Invalid")


if __name__ == "__main__":
    unittest.main()