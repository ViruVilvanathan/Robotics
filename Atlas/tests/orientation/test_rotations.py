from atlas.orientation.rotations import Rotation
import numpy as np
import pytest

init = Rotation(np.array([[0, -1, 0],
                         [-1, 0, 0],
                         [0, 0, 1]]))


def test_rotation_z():
    expected_body = init @ Rotation.rotation_z(np.pi/4)
    expected_world = Rotation.rotation_z(np.pi/4) @ init

    assert np.allclose(init.rotate_body('z', np.pi/4).rotation_matrix, expected_body.rotation_matrix)
    assert np.allclose(init.rotate_world('z', np.pi/4).rotation_matrix, expected_world.rotation_matrix)
    assert not np.allclose(expected_world.rotation_matrix,expected_body.rotation_matrix)

def test_rotation_y():
    expected_body = init @ Rotation.rotation_y(np.pi/2)
    expected_world = Rotation.rotation_y(np.pi/2) @ init

    assert np.allclose(init.rotate_body('y', np.pi/2).rotation_matrix, expected_body.rotation_matrix)
    assert np.allclose(init.rotate_world('y', np.pi/2).rotation_matrix, expected_world.rotation_matrix)
    assert not np.allclose(expected_world.rotation_matrix,expected_body.rotation_matrix)

def test_rotation_x():
    expected_body = init @ Rotation.rotation_x(np.pi/2)
    expected_world = Rotation.rotation_x(np.pi/2) @ init

    assert np.allclose(init.rotate_body('x', np.pi/2).rotation_matrix, expected_body.rotation_matrix)
    assert np.allclose(init.rotate_world('x', np.pi/2).rotation_matrix, expected_world.rotation_matrix)
    assert not np.allclose(expected_world.rotation_matrix,expected_body.rotation_matrix)

def test_invalid_axis():
    with pytest.raises(ValueError):
        init.rotate_body('invalid', np.pi/2)
    with pytest.raises(ValueError):
        init.rotate_world('invalid', np.pi/2)
    