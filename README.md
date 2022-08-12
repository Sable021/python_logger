# python_logger

Custom logger for python using pre-defined logging conventions. This custom logger is mainly adapted from Alexandra Zaharia's custom logger. Blog Link: https://alexandra-zaharia.github.io/posts/custom-logger-in-python-for-stdout-and-or-file-log/

## Log Message Format

All logged messages are following the below format:<br>
<em>{Date Time} | {Log Level} | {File}:{Function} | {Log Message}</em>

## Additional Enhancements Needed
1. Pytest is unable to properly capture log outputs to console. (stdout is captured but it is not stored in the capfd object)
2. Implement mock logger class to abstract away the underlying python logging library. We are only interested in the testing of the logger class and not its dependencies. 
