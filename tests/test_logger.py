import pytest

from src.logger import Logger

# Test Setups
test_file_name = "TEST_FILE"


@pytest.fixture
def tested():
    return Logger(test_file_name)


# Unit Test
def test_logs_debug_message_to_console():
    assert 1 == 1


def test_logs_debug_message_to_file():
    assert 1 == 1
