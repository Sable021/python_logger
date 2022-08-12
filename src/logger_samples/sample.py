"""
Sample python script to observe the use of the custom logger class.
"""
import shutil
from custom_logger.logger import Logger

SAMPLE_LOG_PATH = "logs/"

DEBUG_MSG = "Sample logging to DEBUG level"


def run_sample_logs_console():
    """
    Console logging at various levels. No files are produced
    """

    print("\nStarting Console Logging")
    print("-" * 80)

    # Logger defaults to verbose=True and log_dir=None
    console_log = Logger("console_logger")
    console_log.debug(DEBUG_MSG)


def run_sample_logs_verbose():
    """
    Verbose logging at various levels
    """
    print("\nStarting Verbose Logging")
    print("-" * 80)
    verbose_log = Logger("verbose_logger", verbose=True, log_dir=SAMPLE_LOG_PATH + "verbose_logs")
    verbose_log.debug(DEBUG_MSG)


def run_sample_logs_quiet():
    """
    Quiet logging at various levels
    """

    print("\nStarting Quiet Logging")
    print("-" * 80)

    quiet_log = Logger("quiet_logger", verbose=False, log_dir=SAMPLE_LOG_PATH + "quiet_logs")
    quiet_log.debug(DEBUG_MSG)


def clean_up_created_logs():
    """
    Cleans up the created sample log directory
    """
    print("\n Cleaning Up...")
    shutil.rmtree(SAMPLE_LOG_PATH)


if __name__ == "__main__":
    run_sample_logs_console()
    run_sample_logs_verbose()
    run_sample_logs_quiet()

    # comment this away if you want to see the actual log files
    clean_up_created_logs()
