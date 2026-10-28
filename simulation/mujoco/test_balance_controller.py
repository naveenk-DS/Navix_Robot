import mujoco

from simulation.mujoco.balance_controller import BalanceController


def load_model():
    return mujoco.MjModel.from_xml_path(
        "simulation/mujoco/models/navix_robot.xml"
    )


def test_balance_controller_initialization():
    model = load_model()
    data = mujoco.MjData(model)

    controller = BalanceController(model, data)

    assert controller.orientation_sensor_id >= 0


def test_balance_controller_reads_pitch():
    model = load_model()
    data = mujoco.MjData(model)

    controller = BalanceController(model, data)

    mujoco.mj_forward(model, data)

    pitch = controller.get_pitch()

    assert abs(pitch) < 1.0


def test_balance_controller_update():
    model = load_model()
    data = mujoco.MjData(model)

    controller = BalanceController(model, data)

    mujoco.mj_forward(model, data)

    pitch = controller.update()

    assert isinstance(pitch, float)