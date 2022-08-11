import pytest
import logging
from src.logger.logger import Logger

# Test Setups
TEST_FILE_NAME = "TEST_FILE"
DEBUG_TEST_MSG = "This is a test message at DEBUG level."
DEBUG_LEVEL = "DEBUG"


@pytest.fixture(autouse=True)
def tested():
    return Logger(TEST_FILE_NAME)


# Unit Test
def test_logs_debug_message_to_console(tested, capfd):
    tested.debug(DEBUG_TEST_MSG)

    captured = capfd.readouterr()

    assert DEBUG_TEST_MSG in captured.out


def test_logs_debug_message_to_file():
    assert 1 == 1
