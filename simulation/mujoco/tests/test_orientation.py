from simulation.mujoco.orientation import (
    quaternion_to_pitch,
)


def test_upright_pitch():
    pitch = quaternion_to_pitch(
        [1.0, 0.0, 0.0, 0.0]
    )

    assert abs(pitch) < 0.001


def test_pitch_rotation():
    pitch = quaternion_to_pitch(
        [0.70710678, 0.0, 0.70710678, 0.0]
    )

    assert abs(pitch - 90.0) < 0.01