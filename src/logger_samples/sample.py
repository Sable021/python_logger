"""
Sample python script to observe the use of the custom logger class. Make sure the logger package is already downloaded.
"""
import shutil
from custom_logger.logger import Logger

SAMPLE_LOG_PATH = "logs/"

DEBUG_MSG = "Sample logging to DEBUG level"
INFO_MSG = "Sample logging to INFO level"
WARNING_MSG = "Sample logging to WARNING level"
ERROR_MSG = "Sample logging to ERROR level"
CRITICAL_MSG = "Sample logging to CRITICAL level"
FRAMEWORK_MSG = "Sample logging to FRAMEWORK level"

LEVEL_MSG_LIST = [DEBUG_MSG, INFO_MSG, FRAMEWORK_MSG, WARNING_MSG, ERROR_MSG, CRITICAL_MSG]


def log_messages(logger):
    """Logs messages across all levels to the given logger object"""
    logger_funcs = [logger.debug, logger.info, logger.framework, logger.warning, logger.error, logger.critical]

    for func, msg in zip(logger_funcs, LEVEL_MSG_LIST):
        func(msg)


def run_sample_logs_console():
    """
    Console logging at various levels. No files are produced
    """

    print("\nStarting Console Logging")
    print("-" * 80)

    # Logger defaults to verbose=True and log_dir=None
    console_log = Logger("console_logger")
    log_messages(console_log)


def run_sample_logs_verbose():
    """
    Verbose logging at various levels
    """
    print("\nStarting Verbose Logging")
    print("-" * 80)

    verbose_log = Logger("verbose_logger", log_dir=SAMPLE_LOG_PATH + "verbose_logs", verbose=True)
    log_messages(verbose_log)


def run_sample_logs_quiet():
    """
    Quiet logging at various levels
    """

    print("\nStarting Quiet Logging")
    print("-" * 80)

    quiet_log = Logger("quiet_logger", log_dir=SAMPLE_LOG_PATH + "quiet_logs", verbose=False)
    log_messages(quiet_log)


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
    # clean_up_created_logs()

    print("---------- Sample Run Successful ----------")
