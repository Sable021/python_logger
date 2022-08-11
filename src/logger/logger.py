"""
This module contains the custom logger, Logger, for use across all python projects.
This custom logger is mainly adapted from Alexandra Zaharia's custom logger.
Blog Link: https://alexandra-zaharia.github.io/posts/custom-logger-in-python-for-stdout-and-or-file-log/
"""

import sys

import logging


class Logger(logging.getLoggerClass()):
    """
    Create a custom logger with the specified `name`. When `log_dir` is None, a simple console logger is created.
    Otherwise, a file logger is created in addition to the console logger. This custom logger class adds an extra
    logging level FRAMEWORK (at INFO priority), with the aim of logging messages irrespective of any verbosity settings.
    By default, the five standard logging levels (DEBUG through CRITICAL) only display information in the log file if a
    file handler is added to the logger, but **not** to the console.

    Constants
    ----------
    FRAMEWORK: str
        Custom logging level that will always log to both console and file.

    Parameters
    ----------
    name: str
        Name of logger

    log_dir: str (None)
        The directory for the log file; if not present, no log file is created.

    verbose: bool (True)
        Determines logging verbosity. If true, then all messages get logged both to stdout and to the log file (if
        `log_dir` is specified). If false, then messages only get logged to the log file (if `log_dir` is specified),
        with the exception of FRAMEWORK level messages which get logged either way

    Methods
    ----------
    debug(msg: str, *args, **kwargs):
        Logs a message at the debug level.
    """

    FRAMEWORK = "FRAMEWORK"
    STDOUT_LOG_FORMAT = "%(message)s"
    FILE_LOG_FORMAT = "%(asctime)s | %(levelname)9s | %(filename)s:%(lineno)d | %(message)s"

    def __init__(self, name, log_dir=None, verbose=True):
        # Create custom logger logging all five levels
        super().__init__(name)
        self.setLevel(logging.DEBUG)

        # Add new logging level
        logging.addLevelName(logging.INFO, self.FRAMEWORK)

        # Determine verbosity settings
        self.verbose = verbose

        # Create stream handler for logging to stdout (log all five levels)
        self.stdout_handler = logging.StreamHandler(sys.stdout)
        self.stdout_handler.setLevel(logging.DEBUG)
        # TODO: update stdout logging format
        self.stdout_handler.setFormatter(logging.Formatter(self.STDOUT_LOG_FORMAT))
        self._enable_console_output()

    def _has_console_handler(self):
        return len([h for h in self.handlers if h.isinstance(logging.StreamHandler)]) > 0

    def _enable_console_output(self):
        if self._has_console_handler():
            return
        self.addHandler(self.stdout_handler)

    def _custom_log(self, func, msg, *args, **kwargs):
        """
        Helper method for logging DEBUG through CRITICAL messages by calling the appropriate `func()` from the base
        class.
        """
        # Log normally if verbosity is on
        if self.verbose:
            return func(msg, *args, **kwargs)

        # If verbosity is off and there is no file handler, there is nothing left to do
        # TODO implement block

        # If verbosity is off and a file handler is present, then disable stdout logging, log and finally reenable
        # stdout logging
        # TODO implement block

    def debug(self, msg, *args, **kwargs):
        print(msg)
        # self._custom_log(super().debug, msg, *args, **kwargs)
