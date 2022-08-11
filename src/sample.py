"""
Sample python script to observe the use of the custom logger class.
"""

from logger.logger import Logger


def run_sample_logs():
    """
    Verbose logging at various levels
    """
    print("Starting Sample Logging")
    print("-" * 80)
    verbose_log = Logger("verbose", verbose=True, log_dir="logs")

    verbose_log.debug("Sample logging to DEBUG level")


if __name__ == "__main__":
    run_sample_logs()
