import unittest

from calendar_solver.calendar_solver.tetrino import InvalidShapeError, Shape, Tetrino


class TestTetrino(unittest.TestCase):
    def setUp(self):
        """
        Set up test data for Tetrino pieces.
        """
        self.tetrinos = {
            "small_L_tetrino": Tetrino(Shape(2, 3, [[1, 0], [1, 0], [1, 1]]), "sL"),
            "big_L_tetrino": Tetrino(Shape(2, 4, [[1, 0], [1, 0], [1, 0], [1, 1]]), "bL"),
            "symmetrical_L_tetrino": Tetrino(Shape(3, 3, [[1, 0, 0], [1, 0, 0], [1, 1, 1]]), "symL"),
            "lowercase_l_tetrino": Tetrino(Shape(1, 4, [[1], [1], [1], [1]]), "l"),
            "u_tetrino": Tetrino(Shape(3, 2, [[1, 0, 1], [1, 1, 1]]), "U"),
            "small_z_tetrino": Tetrino(Shape(3, 2, [[1, 1, 0], [0, 1, 1]]), "sZ"),
            "big_z_tetrino": Tetrino(Shape(4, 2, [[0, 0, 1, 1], [1, 1, 1, 0]]), "bZ"),
            "z_tetrino": Tetrino(Shape(3, 3, [[0, 1, 1], [0, 1, 0], [1, 1, 0]]), "Z"),
            "t_tetrino": Tetrino(Shape(3, 3, [[1, 1, 1], [0, 1, 0], [0, 1, 0]]), "T"),
            "p_tetrino": Tetrino(Shape(2, 3, [[1, 1], [1, 1], [1, 0]]), "P"),
        }

    def test_initial_shape(self):
        """
        Test the initial shape of the Tetrinos.
        """
        for name, tetrino in self.tetrinos.items():
            with self.subTest(tetrino=name):
                expected_shape = tetrino.shape.shape
                self.assertEqual(tetrino.shape.shape, expected_shape)

    def test_rotate_90(self):
        """
        Test rotating the Tetrino 90 degrees clockwise.
        """
        self.small_L_tetrino = self.tetrinos["small_L_tetrino"]
        self.small_L_tetrino.rotate_clockwise(90)
        expected_shape = [[1, 1, 1], [1, 0, 0]]
        self.assertEqual(self.small_L_tetrino.shape.shape, expected_shape)
        
        self.big_L_tetrino = self.tetrinos["big_L_tetrino"]
        self.big_L_tetrino.rotate_clockwise(90)
        expected_shape = [[1, 1, 1, 1], [1, 0, 0, 0]]
        self.assertEqual(self.big_L_tetrino.shape.shape, expected_shape)
        
        self.symmetrical_L_tetrino = self.tetrinos["symmetrical_L_tetrino"]
        self.symmetrical_L_tetrino.rotate_clockwise(90)
        expected_shape = [[1, 1, 1], [1, 0, 0], [1, 0, 0]]
        self.assertEqual(self.symmetrical_L_tetrino.shape.shape, expected_shape)
        
        self.lowercase_l_tetrino = self.tetrinos["lowercase_l_tetrino"]
        self.lowercase_l_tetrino.rotate_clockwise(90)
        expected_shape = [[1, 1, 1, 1]]
        self.assertEqual(self.lowercase_l_tetrino.shape.shape, expected_shape)
        
        self.u_tetrino = self.tetrinos["u_tetrino"]
        self.u_tetrino.rotate_clockwise(90)
        expected_shape = [[1, 1], [1, 0], [1, 1]]
        self.assertEqual(self.u_tetrino.shape.shape, expected_shape)
        
        self.small_z_tetrino = self.tetrinos["small_z_tetrino"]
        self.small_z_tetrino.rotate_clockwise(90)
        expected_shape = [[0, 1], [1, 1], [1, 0]]
        self.assertEqual(self.small_z_tetrino.shape.shape, expected_shape)
        
        self.big_z_tetrino = self.tetrinos["big_z_tetrino"]
        self.big_z_tetrino.rotate_clockwise(90)
        expected_shape = [[1, 0], [1, 0], [1, 1], [0, 1]]
        self.assertEqual(self.big_z_tetrino.shape.shape, expected_shape)
        
        self.z_tetrino = self.tetrinos["z_tetrino"]
        self.z_tetrino.rotate_clockwise(90)
        expected_shape = [[1, 0, 0], [1, 1, 1], [0, 0, 1]]
        self.assertEqual(self.z_tetrino.shape.shape, expected_shape)
        
        self.t_tetrino = self.tetrinos["t_tetrino"]
        self.t_tetrino.rotate_clockwise(90)
        expected_shape = [[0, 0, 1], [1, 1, 1], [0, 0, 1]]
        self.assertEqual(self.t_tetrino.shape.shape, expected_shape)
        
        self.p_tetrino = self.tetrinos["p_tetrino"]
        self.p_tetrino.rotate_clockwise(90)
        expected_shape = [[1, 1, 1], [0, 1, 1]]
        self.assertEqual(self.p_tetrino.shape.shape, expected_shape)

    def test_rotate_180(self):
        """
        Test rotating the Tetrino 180 degrees clockwise.
        """
        self.small_L_tetrino = self.tetrinos["small_L_tetrino"]
        self.small_L_tetrino.rotate_clockwise(180)
        expected_shape = [[1, 1], [0, 1], [0, 1]]
        self.assertEqual(self.small_L_tetrino.shape.shape, expected_shape)
        
        self.big_L_tetrino = self.tetrinos["big_L_tetrino"]
        self.big_L_tetrino.rotate_clockwise(180)
        expected_shape = [[1, 1], [0, 1], [0, 1], [0, 1]]
        self.assertEqual(self.big_L_tetrino.shape.shape, expected_shape)
        
        self.symmetrical_L_tetrino = self.tetrinos["symmetrical_L_tetrino"]
        self.symmetrical_L_tetrino.rotate_clockwise(180)
        expected_shape = [[1, 1, 1], [0, 0, 1], [0, 0, 1]]
        self.assertEqual(self.symmetrical_L_tetrino.shape.shape, expected_shape)
        
        self.lowercase_l_tetrino = self.tetrinos["lowercase_l_tetrino"]
        self.lowercase_l_tetrino.rotate_clockwise(180)
        expected_shape = [[1], [1], [1], [1]]
        self.assertEqual(self.lowercase_l_tetrino.shape.shape, expected_shape)
        
        self.u_tetrino = self.tetrinos["u_tetrino"]
        self.u_tetrino.rotate_clockwise(180)
        expected_shape = [[1, 1, 1], [1, 0, 1]]
        self.assertEqual(self.u_tetrino.shape.shape, expected_shape)
        
        self.small_z_tetrino = self.tetrinos["small_z_tetrino"]
        self.small_z_tetrino.rotate_clockwise(180)
        expected_shape = [[1, 1, 0], [0, 1, 1]]
        self.assertEqual(self.small_z_tetrino.shape.shape, expected_shape)
        
        self.big_z_tetrino = self.tetrinos["big_z_tetrino"]
        self.big_z_tetrino.rotate_clockwise(180)
        expected_shape = [[0, 1, 1, 1], [1, 1, 0, 0]]
        self.assertEqual(self.big_z_tetrino.shape.shape, expected_shape)
        
        self.z_tetrino = self.tetrinos["z_tetrino"]
        self.z_tetrino.rotate_clockwise(180)
        expected_shape = [[0, 1, 1], [0, 1, 0], [1, 1, 0]]
        self.assertEqual(self.z_tetrino.shape.shape, expected_shape)
        
        self.t_tetrino = self.tetrinos["t_tetrino"]
        self.t_tetrino.rotate_clockwise(180)
        expected_shape = [[0, 1, 0], [0, 1, 0], [1, 1, 1]]
        self.assertEqual(self.t_tetrino.shape.shape, expected_shape)
        
        self.p_tetrino = self.tetrinos["p_tetrino"]
        self.p_tetrino.rotate_clockwise(180)
        expected_shape = [[0, 1], [1, 1], [1, 1]]
        self.assertEqual(self.p_tetrino.shape.shape, expected_shape)

    def test_rotate_360(self):
        """
        Test rotating the Tetrino 360 degrees clockwise (full rotation).
        """
        self.small_L_tetrino = self.tetrinos["small_L_tetrino"]
        self.small_L_tetrino.rotate_clockwise(360)
        expected_shape = [[1, 0], [1, 0], [1, 1]]  # Should return to the original shape
        self.assertEqual(self.small_L_tetrino.shape.shape, expected_shape)
        
        self.big_L_tetrino = self.tetrinos["big_L_tetrino"]
        self.big_L_tetrino.rotate_clockwise(360)
        expected_shape = [[1, 0], [1, 0], [1, 0], [1, 1]]
        self.assertEqual(self.big_L_tetrino.shape.shape, expected_shape)
        
        self.symmetrical_L_tetrino = self.tetrinos["symmetrical_L_tetrino"]
        self.symmetrical_L_tetrino.rotate_clockwise(360)
        expected_shape = [[1, 0, 0], [1, 0, 0], [1, 1, 1]]
        self.assertEqual(self.symmetrical_L_tetrino.shape.shape, expected_shape)
        
        self.lowercase_l_tetrino = self.tetrinos["lowercase_l_tetrino"]
        self.lowercase_l_tetrino.rotate_clockwise(360)
        expected_shape = [[1], [1], [1], [1]]
        self.assertEqual(self.lowercase_l_tetrino.shape.shape, expected_shape)
        
        self.u_tetrino = self.tetrinos["u_tetrino"]
        self.u_tetrino.rotate_clockwise(360)
        expected_shape = [[1, 0, 1], [1, 1, 1]]
        self.assertEqual(self.u_tetrino.shape.shape, expected_shape)
        
        self.small_z_tetrino = self.tetrinos["small_z_tetrino"]
        self.small_z_tetrino.rotate_clockwise(360)
        expected_shape = [[1, 1, 0], [0, 1, 1]]
        self.assertEqual(self.small_z_tetrino.shape.shape, expected_shape)
        
        self.big_z_tetrino = self.tetrinos["big_z_tetrino"]
        self.big_z_tetrino.rotate_clockwise(360)
        expected_shape = [[0, 0, 1, 1], [1, 1, 1, 0]]
        self.assertEqual(self.big_z_tetrino.shape.shape, expected_shape)
        
        self.z_tetrino = self.tetrinos["z_tetrino"]
        self.z_tetrino.rotate_clockwise(360)
        expected_shape = [[0, 1, 1], [0, 1, 0], [1, 1, 0]]
        self.assertEqual(self.z_tetrino.shape.shape, expected_shape)
        
        self.t_tetrino = self.tetrinos["t_tetrino"]
        self.t_tetrino.rotate_clockwise(360)
        expected_shape = [[1, 1, 1], [0, 1, 0], [0, 1, 0]]
        self.assertEqual(self.t_tetrino.shape.shape, expected_shape)
        
        self.p_tetrino = self.tetrinos["p_tetrino"]
        self.p_tetrino.rotate_clockwise(360)
        expected_shape = [[1, 1], [1, 1], [1, 0]]
        self.assertEqual(self.p_tetrino.shape.shape, expected_shape)
        
    def test_invalid_shape(self):
        """
        Test that an invalid shape raises an InvalidShapeError.
        """
        with self.assertRaises(InvalidShapeError):
            Tetrino(Shape(2, 3, [[1, 0], [1, 0]]), "Invalid")


if __name__ == "__main__":
    unittest.main()