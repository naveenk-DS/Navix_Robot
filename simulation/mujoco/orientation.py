import math


def quaternion_to_pitch(
    quaternion: list[float],
) -> float:
    """Convert MuJoCo quaternion [w, x, y, z] to pitch in degrees."""

    w, x, y, z = quaternion

    sin_pitch = 2.0 * (w * y - z * x)

    sin_pitch = max(-1.0, min(1.0, sin_pitch))

    pitch = math.asin(sin_pitch)

    return math.degrees(pitch)