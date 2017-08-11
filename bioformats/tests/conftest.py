import javabridge
import pytest

import bioformats


@pytest.fixture(autouse=True, scope="session")
def setup_and_teardown():
    javabridge.start_vm(class_path=bioformats.JARS)

    yield

    javabridge.kill_vm()
