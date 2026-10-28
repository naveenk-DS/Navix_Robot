import mujoco


def test_mujoco_is_available():
    model = mujoco.MjModel.from_xml_string(
        """
        <mujoco>
            <worldbody>
                <body name="box" pos="0 0 1">
                    <freejoint/>
                    <geom type="box" size="0.1 0.1 0.1"/>
                </body>
            </worldbody>
        </mujoco>
        """
    )

    data = mujoco.MjData(model)

    mujoco.mj_step(model, data)

    assert model.nbody == 2
    assert data.time > 0
