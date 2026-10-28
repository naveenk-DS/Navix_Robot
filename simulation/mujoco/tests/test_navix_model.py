from pathlib import Path

import mujoco


MODEL_PATH = (
    Path(__file__).resolve().parent
    / "models"
    / "navix_robot.xml"
)


def test_navix_model_loads():
    model = mujoco.MjModel.from_xml_path(str(MODEL_PATH))
    data = mujoco.MjData(model)

    mujoco.mj_step(model, data)

    assert model.nbody > 1
    assert model.njnt >= 4
    assert model.nu == 6
    assert data.time > 0
