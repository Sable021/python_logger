"""
This module contains the custom logger, Logger, for use across all python projects.
This custom logger is mainly adapted from Alexandra Zaharia's custom logger.
Blog Link: https://alexandra-zaharia.github.io/posts/custom-logger-in-python-for-stdout-and-or-file-log/
"""

import logging


class Logger(logging.getLoggerClass()):
    """
    Create a custom logger with the specified `name`. When `log_dir` is None, a simple console logger is created.
    Otherwise, a file logger is created in addition to the console logger.
    This custom logger class adds an extra logging level FRAMEWORK (at INFO priority), with the aim of logging messages
    irrespective of any verbosity settings. By default, the five standard logging levels (DEBUG through CRITICAL) only
    display information in the log file if a file handler is added to the logger, but **not** to the console.

    """

    def __init__(self, name):
        super().__init__(name)
