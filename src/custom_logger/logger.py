"""
This module contains the custom logger, Logger, for use across all python projects.
This custom logger is mainly adapted from Alexandra Zaharia's custom logger.
Blog Link: https://alexandra-zaharia.github.io/posts/custom-logger-in-python-for-stdout-and-or-file-log/
"""

import os
import sys
import datetime
import logging


class Logger(logging.getLoggerClass()):
    """
    Create a custom logger with the specified `name`. When `log_dir` is None, a simple console logger is created.
    Otherwise, a file logger is created in addition to the console logger. This custom logger class adds an extra
    logging level FRAMEWORK (at INFO+1 priority), with the aim of logging messages irrespective of any verbosity
    settings. By default, the five standard logging levels (DEBUG through CRITICAL) only display information in the log
    file if a file handler is added to the logger, but **not** to the console.

    Constants
    ----------
    FRAMEWORK: str
        Custom logging level that will always log to both console and file.

    STDOUT_LOG_FORMAT: str
        Defined logging format for console output.

    FILE_LOG_FORMAT: str
        Defined logging format for file output.

    DATETIME_FORMAT: str
        Defined format for list date and time of log messages.

    CALL_STACK_LEVEL: int
        This value is set to 3 for the python logger to retrieve the actual calling function and not this wrapper.

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

    info(msg: str, *args, **kwargs):
        Logs a message at the info level.

    warning(msg: str, *args, **kwargs):
        Logs a message at the warning level.

    error(msg: str, *args, **kwargs):
        Logs a message at the error level.

    critical(msg: str, *args, **kwargs):
        Logs a message at the critical level.

    framework(msg: str, *args, **kwargs):
        Logs a message at the framework level.

    pause():
        Pauses file output of the logger.

    resume():
        Resumes file logging.
    """

    FRAMEWORK = "FRAMEWORK"
    FRAMEWORK_LEVEL = 21
    STDOUT_LOG_FORMAT = "%(asctime)s | %(levelname)9s | %(filename)s:%(funcName)s | %(message)s"
    FILE_LOG_FORMAT = "%(asctime)s | %(levelname)9s | %(filename)s:%(funcName)s | %(message)s"
    DATETIME_FORMAT = "%d-%b-%Y %H:%M:%S"

    # Stacklevel is set to to ensure logger logs actual calling function and not this class
    CALL_STACK_LEVEL = 3

    def __init__(self, name, log_dir=None, verbose=True):
        # Create custom logger logging all five levels
        super().__init__(name)
        self.setLevel(logging.DEBUG)

        # Add new logging level
        logging.addLevelName(self.FRAMEWORK_LEVEL, self.FRAMEWORK)

        # Determine verbosity settings
        self.verbose = verbose

        # Create stream handler for logging to stdout (log all levels)
        self.stdout_handler = logging.StreamHandler(sys.stdout)
        self.stdout_handler.setLevel(logging.DEBUG)
        self.stdout_handler.setFormatter(logging.Formatter(self.STDOUT_LOG_FORMAT))
        self._enable_console_output()

        self.file_handler = None
        if log_dir:
            self._add_file_handler(name, log_dir)

    def _has_console_handler(self):
        # pylint: disable=unidiomatic-typecheck
        # Only interested in the exact object type and not the inherited types. (i.e., FileHandler)
        return len([h for h in self.handlers if type(h) is logging.StreamHandler]) > 0

    def _has_file_handler(self):
        return len([h for h in self.handlers if isinstance(h, logging.FileHandler)]) > 0

    def _enable_console_output(self):
        if self._has_console_handler():
            return
        self.addHandler(self.stdout_handler)

    def _disable_console_output(self):
        if not self._has_console_handler():
            return
        self.removeHandler(self.stdout_handler)

    def _add_file_handler(self, name, log_dir):
        """Add a file handler for this logger with the specified <name> (and store the log file under <log_dir>)."""

        # Format for file log
        formatter = logging.Formatter(self.FILE_LOG_FORMAT, self.DATETIME_FORMAT)

        # Determine log path and file name, create log path if it does not exist
        now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        log_name = f"{str(name).replace(' ', '_')}_{now}"
        if not os.path.exists(log_dir):
            try:
                os.makedirs(log_dir)
            # Types of errors that will be raised if directory cannot be created.
            except (NotADirectoryError, PermissionError):
                print(f"{self.__class__.__name__}: Cannot create directory {log_dir}.", end="", file=sys.stderr)
                log_dir = "/tmp" if sys.platform.startswith("linux") else "."
                print(f"Defaulting to {log_dir}.", file=sys.stderr)

        log_file = os.path.join(log_dir, log_name) + ".log"

        # Create file handler for logging to a file (log all five levels)
        self.file_handler = logging.FileHandler(log_file)
        self.file_handler.setLevel(logging.DEBUG)
        self.file_handler.setFormatter(formatter)
        self.addHandler(self.file_handler)

    def _custom_log(self, func, msg, *args, **kwargs):
        """
        Helper method for logging DEBUG through CRITICAL messages by calling the appropriate `func()` from the base
        class.
        """
        # Log normally if verbosity is on
        if self.verbose:
            return func(msg, *args, **kwargs)

        # If verbosity is off and a file handler is present, then disable stdout logging, log and finally reenable
        # stdout logging
        if self._has_file_handler():
            self._disable_console_output()
            func(msg, *args, **kwargs)
            self._enable_console_output()
            return None

        # If verbosity is off and there is no file handler, there is nothing left to do
        return None

    def debug(self, msg, *args, **kwargs):
        """
        Logs message at debug level.

        Parameters
        ----------
        msg: str
            Message to be logged.
        """
        self._custom_log(super().debug, msg, stacklevel=self.CALL_STACK_LEVEL, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        """
        Logs message at info level.

        Parameters
        ----------
        msg: str
            Message to be logged.
        """
        self._custom_log(super().info, msg, stacklevel=self.CALL_STACK_LEVEL, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        """
        Logs message at warning level.

        Parameters
        ----------
        msg: str
            Message to be logged.
        """
        self._custom_log(super().warning, msg, stacklevel=self.CALL_STACK_LEVEL, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        """
        Logs message at error level.

        Parameters
        ----------
        msg: str
            Message to be logged.
        """
        self._custom_log(super().error, msg, stacklevel=self.CALL_STACK_LEVEL, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        """
        Logs message at critical level

        Parameters
        ----------
        msg: str
            Message to be logged.
        """
        self._custom_log(super().critical, msg, stacklevel=self.CALL_STACK_LEVEL, *args, **kwargs)

    def framework(self, msg, *args, **kwargs):
        """
        Logs message at framework level. The `msg` gets logged both to stdout and to file (if a file handler is
        present), irrespective of verbosity settings.

        Parameters
        ----------
        msg: str
            Message to be logged.
        """

        # Call stack is reduced by 1 as the wrapper function is not used
        stack_level = self.CALL_STACK_LEVEL - 1

        super().log(self.FRAMEWORK_LEVEL, msg, stacklevel=stack_level, *args, **kwargs)

    def pause(self):
        """Pauses file output of the logger."""
        if self._has_file_handler():
            self.removeHandler(self.file_handler)

    def resume(self):
        """Resumes file logging"""
        if not self._has_file_handler():
            self.addHandler(self.file_handler)
