"""
KNOWN ISSUES
--------------------
1. Unable to test correctness of console output. Pytest's capfd and capsys doesn't seem to properly 
    capture log outputs to consoles.
"""
import os
import shutil
import glob
import pytest
from src.logger.logger import Logger

# Test Setups
TEST_LOG_PATH = "./tests/test_files/"
TEST_FILE_NAME = "TEST_FILE"
DEBUG_TEST_MSG = "This is a test message at DEBUG level."
DEBUG_LEVEL = "DEBUG"


@pytest.fixture(autouse=True)
def logger_console():
    return Logger(TEST_FILE_NAME, verbose=True, log_dir=None)


@pytest.fixture
def logger_file():
    logger = Logger(TEST_FILE_NAME, verbose=False, log_dir=TEST_LOG_PATH)
    return logger


@pytest.fixture
def logger_console_file():
    return Logger(TEST_FILE_NAME, verbose=True, log_dir=TEST_LOG_PATH)


def clean_test_log_dir():
    shutil.rmtree(TEST_LOG_PATH)


# Unit Tests

# Defective test: capfd doesn't hold the stdout text even though stdout is captured.
# def test_logs_debug_message_to_stdout(tested_console, capfd):
#     tested_console.debug(DEBUG_TEST_MSG)
#     captured = capfd.readouterr()

#     # Assert both log level and msg are captured
#     assert DEBUG_LEVEL in captured.out
#     assert DEBUG_TEST_MSG in captured.out


def test_logs_debug_message_to_new_file(logger_file, tmpdir):
    function_name = str(test_logs_debug_message_to_new_file.__name__)
    module_file_name = str(os.path.basename(__file__))

    logger_file.debug(DEBUG_TEST_MSG)

    # Assert file dir exists
    assert os.path.exists(TEST_LOG_PATH)

    # Find latest file
    files_list = glob.glob(TEST_LOG_PATH + "/*")
    actual_file = max(files_list, key=os.path.getctime)

    # Assert file name contains given name
    assert TEST_FILE_NAME in actual_file

    # Assert contents of file are correct
    with open(actual_file, "r") as f:
        actual_logged = f.readline()
        assert function_name in actual_logged
        assert module_file_name in actual_logged
        assert DEBUG_LEVEL in actual_logged
        assert DEBUG_TEST_MSG in actual_logged


# Final test cleanup. Comment code if contents of test log folder needs to be seen
def test_cleanup():
    clean_test_log_dir()
