import os

import javabridge
import pytest

import bioformats


@pytest.fixture(autouse=True, scope="session")
def setup_and_teardown():
    log_config = os.path.join(os.path.split(__file__)[0], "resources", "log4j.properties")

    javabridge.start_vm(
        args=[
            "-Dlog4j.configuration=file:{}".format(log_config),
        ],
        class_path=bioformats.JARS,
        run_headless=True
    )

    yield

    javabridge.kill_vm()
