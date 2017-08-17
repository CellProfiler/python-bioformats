import javabridge
import pytest

import bioformats


@pytest.fixture(autouse=True, scope="session")
def setup_and_teardown():
    javabridge.start_vm(class_path=bioformats.JARS, run_headless=True)

    yield

    javabridge.kill_vm()
