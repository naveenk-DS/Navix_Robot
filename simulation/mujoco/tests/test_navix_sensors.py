from pathlib import Path

import mujoco


MODEL_PATH = (
    Path(__file__).resolve().parent
    / "models"
    / "navix_robot.xml"
)


def test_navix_sensors():
    model = mujoco.MjModel.from_xml_path(str(MODEL_PATH))
    data = mujoco.MjData(model)

    mujoco.mj_step(model, data)

    assert model.nsensor > 0

    print("\nNAVIX sensors:")

    for sensor_id in range(model.nsensor):
        name = mujoco.mj_id2name(
            model,
            mujoco.mjtObj.mjOBJ_SENSOR,
            sensor_id,
        )

        print(
            f"  {sensor_id}: "
            f"{name}"
        )

    print("\nSensor values:")

    for sensor_id in range(model.nsensor):
        address = model.sensor_adr[sensor_id]
        dimension = model.sensor_dim[sensor_id]

        values = data.sensordata[
            address:address + dimension
        ]

        print(f"  {sensor_id}: {values}")

    assert model.nsensor == 15