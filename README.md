# Logger for Python Projects
Custom logger for python using pre-defined logging conventions. This custom logger is mainly adapted from Alexandra Zaharia's custom logger. Blog Link: https://alexandra-zaharia.github.io/posts/custom-logger-in-python-for-stdout-and-or-file-log/

## Project Setup
Download the project into your IDE environment. Install all required packages in the devt_requirement.txt file.

## Log Message Format
All logged messages are following the below format:<br>
<em>{Date Time} | {Log Level} | {File}:{Function} | {Log Message}</em>

## Eample Code Usage
```python
logger = Logger('logger_name', verbose=True, log_dir'log_path')
logger.debug('Debug Message')
```

## Unit Testing and Coverage
This project uses pytest and coverage libraries for unit testing and coverage report. To run testing, run <em>python -m pytest</em> at the root folder of the project. It will recursively search for all functions with test_ as a prefix and run them. For the coverage report, first run <em>coverage run -m pytest</em> and then <em>\"coverage report --omit="\*/test\*\"</em> or <em>\"coverage html --omit="\*/test\*\"</em> to get the report in html form. The <em>--omit</em> flag indicates that the test folder should not be included.

## Packaging Instructions
Packaing information is found in pyproject.toml and setup.cfg. Run the following commands at root folder:
1. <em>python -m build</em> (Create packages in dist folder)
2. <em>python -m twine upload --repository testpypi dist/\*\<version_number\>\*</em> (Repository flag determines which library repo you are uploading your package to and it is good practice to be specific with what you are uploading.)

<p>You can test the package by creating a new venv environment, importing the new package, and then running src/logger_samples/sample.py file to check logging status.</p>


## Code Refactoring Needed
1. Pytest is unable to properly capture log outputs to console. (stdout is captured but it is not stored in the capfd object)
2. Implement mock logger class to abstract away the underlying python logging library. We are only interested in the testing of the logger class and not its dependencies. 

## Possible Enhancements
1. Re-open last log file to continue
2. Log file rolling (prevents log file from becoming too big)
3. Allow user chosen lowest logging level (currently internally fixed at DEBUG)
