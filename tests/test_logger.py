"""
KNOWN ISSUES
--------------------
1. Unable to test correctness of console output. Pytest's capfd and capsys doesn't seem to properly 
    capture log outputs to consoles.
    a. Unable to correctly test wrapper capability of logging to file but not console\
2. No convenient way to test directory creation exceptions. 
"""
import os
import shutil
import glob
import pytest
from src.custom_logger.logger import Logger

# Test Setups
TEST_LOG_PATH = "./tests/test_files/"
TEST_FILE_NAME = "TEST_FILE"
MODULE_FILE_NAME = os.path.basename(__file__)

# Log Levels
DEBUG_LEVEL = "DEBUG"
INFO_LEVEL = "INFO"
WARNING_LEVEL = "WARNING"
ERROR_LEVEL = "ERROR"
CRITICAL_LEVEL = "CRITICAL"
FRAMEWORK_LEVEL = "FRAMEWORK"

# Create Test Messages
def create_test_msg(log_level):
    return f"This is a test message at {log_level} level."


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
    if os.path.exists(TEST_LOG_PATH):
        shutil.rmtree(TEST_LOG_PATH)


# Internal Methods
def find_latest_file(file_path):
    files_list = glob.glob(TEST_LOG_PATH + "/*")
    actual_file = max(files_list, key=os.path.getctime)

    return actual_file


def check_file_content(actual_file, expected_name, level, func_name, expected_msg):
    # Assert file name contains given name
    assert expected_name in actual_file

    # Assert contents of file are correct
    with open(actual_file, "rb") as f:
        num_lines = sum(1 for _ in f)
        # Find last line of file. Refer to below link
        # https://www.codingem.com/how-to-read-the-last-line-of-a-file-in-python/
        try:  # catch OSError in case of a one line file
            f.seek(-2, os.SEEK_END)
            while f.read(1) != b"\n":
                f.seek(-2, os.SEEK_CUR)
        except OSError:
            f.seek(0)
        actual_logged = f.readline().decode()

        # Log level appears twice, once when stating level and once within the message.
        assert actual_logged.count(level) == 2
        assert MODULE_FILE_NAME in actual_logged
        assert func_name in actual_logged
        assert expected_msg in actual_logged

    f.close()

    return num_lines


def check_dir_file_latest_content(dir_path, expected_name, level, func_name, expected_msg):
    assert os.path.exists(dir_path)
    actual_file = find_latest_file(dir_path)
    check_file_content(actual_file, expected_name, level, func_name, expected_msg)


# Unit Tests
@pytest.mark.skip(reason="Cannot test: capfd doesn't hold the stdout text even though stdout is captured.")
def test_logs_debug_message_to_stdout(tested_console, capfd):
    expected_test_msg = create_test_msg(DEBUG_LEVEL)
    tested_console.debug(expected_test_msg)
    captured = capfd.readouterr()

    # Assert both log level and msg are captured
    assert DEBUG_LEVEL in captured.out
    assert expected_test_msg in captured.out


def test_does_not_log_message_to_file_if_log_dir_empty(logger_console):
    clean_test_log_dir()
    logger_console.debug(create_test_msg(DEBUG_LEVEL))
    logger_console.info(create_test_msg(INFO_LEVEL))
    logger_console.warning(create_test_msg(WARNING_LEVEL))
    logger_console.error(create_test_msg(ERROR_LEVEL))
    logger_console.critical(create_test_msg(CRITICAL_LEVEL))
    logger_console.framework(create_test_msg(FRAMEWORK_LEVEL))

    # Assert log directory does not exist
    assert os.path.exists(TEST_LOG_PATH) == False


def test_logs_debug_message_to_file(logger_file):
    function_name = str(test_logs_debug_message_to_file.__name__)
    expected_test_msg = create_test_msg(DEBUG_LEVEL)

    logger_file.debug(expected_test_msg)

    check_dir_file_latest_content(TEST_LOG_PATH, TEST_FILE_NAME, DEBUG_LEVEL, function_name, expected_test_msg)


def test_logs_info_message_to_file(logger_file):
    function_name = str(test_logs_info_message_to_file.__name__)
    expected_test_msg = create_test_msg(INFO_LEVEL)

    logger_file.info(expected_test_msg)

    check_dir_file_latest_content(TEST_LOG_PATH, TEST_FILE_NAME, INFO_LEVEL, function_name, expected_test_msg)


def test_logs_warning_message_to_file(logger_file):
    function_name = str(test_logs_warning_message_to_file.__name__)
    expected_test_msg = create_test_msg(WARNING_LEVEL)

    logger_file.warning(expected_test_msg)

    check_dir_file_latest_content(TEST_LOG_PATH, TEST_FILE_NAME, WARNING_LEVEL, function_name, expected_test_msg)


def test_logs_error_message_to_file(logger_file):
    function_name = str(test_logs_error_message_to_file.__name__)
    expected_test_msg = create_test_msg(ERROR_LEVEL)

    logger_file.error(expected_test_msg)

    check_dir_file_latest_content(TEST_LOG_PATH, TEST_FILE_NAME, ERROR_LEVEL, function_name, expected_test_msg)


def test_logs_critical_message_to_file(logger_file):
    function_name = str(test_logs_critical_message_to_file.__name__)
    expected_test_msg = create_test_msg(CRITICAL_LEVEL)

    logger_file.critical(expected_test_msg)

    check_dir_file_latest_content(TEST_LOG_PATH, TEST_FILE_NAME, CRITICAL_LEVEL, function_name, expected_test_msg)


def test_logs_framework_message_to_file(logger_file):
    function_name = str(test_logs_framework_message_to_file.__name__)
    expected_test_msg = create_test_msg(FRAMEWORK_LEVEL)

    logger_file.framework(expected_test_msg)

    check_dir_file_latest_content(TEST_LOG_PATH, TEST_FILE_NAME, FRAMEWORK_LEVEL, function_name, expected_test_msg)


def test_logs_do_not_write_to_file_on_pause(logger_file):
    function_name = str(test_logs_do_not_write_to_file_on_pause.__name__)

    # Write initial msg as baseline
    initial_msg = f"Initial {INFO_LEVEL} message."
    logger_file.info(initial_msg)
    expected_num_lines = check_dir_file_latest_content(
        TEST_LOG_PATH, TEST_FILE_NAME, INFO_LEVEL, function_name, initial_msg
    )

    logger_file.pause()

    # Write new message and check latest log is still at inital message.
    unlog_msg = f"This message at {WARNING_LEVEL} should not be seen!"
    logger_file.warning(unlog_msg)

    actual_log_file = find_latest_file(TEST_LOG_PATH)
    actual_num_lines = sum(1 for _ in open(actual_log_file))
    check_dir_file_latest_content(TEST_LOG_PATH, TEST_FILE_NAME, INFO_LEVEL, function_name, initial_msg)


def test_logs_write_to_file_on_resume(logger_file):
    test_logs_do_not_write_to_file_on_pause(logger_file)

    logger_file.resume()

    resume_func = str(test_logs_write_to_file_on_resume.__name__)
    resume_msg = f"This message at {CRITICAL_LEVEL} should be logged on resume."
    logger_file.critical(resume_msg)

    check_dir_file_latest_content(TEST_LOG_PATH, TEST_FILE_NAME, CRITICAL_LEVEL, resume_func, resume_msg)


def test_will_not_throw_exist_if_directory_already_exists(logger_file):
    dup_file_name = "duplicate"
    dup_logger = Logger(dup_file_name, TEST_LOG_PATH, verbose=False)
    function_name = str(test_will_not_throw_exist_if_directory_already_exists.__name__)
    expected_test_msg = create_test_msg(DEBUG_LEVEL)

    dup_logger.debug(expected_test_msg)

    check_dir_file_latest_content(TEST_LOG_PATH, dup_file_name, DEBUG_LEVEL, function_name, expected_test_msg)


# Final test cleanup. Comment code if contents of test log folder needs to be seen
def test_cleanup():
    clean_test_log_dir()
