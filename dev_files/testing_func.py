import logging


color_codes = {
    "reset": "\033[0m",  # add at the end to stop coloring
    "black": "\033[30m",
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "white": "\033[37m",
}

BOLD_SEQ = "\033[1m"


class MyFormatter(logging.Formatter):
    """

    %(module)s:
    %(lineno)d:
    %(msg)s
    """

    def __init__(self):
        super().__init__(fmt="%(levelno)d: %(msg)s", datefmt=None, style='%')

    def format(self, record):
        # Save the original format configured by the user when the logger formatter was instantiated
        format_orig = self._style._fmt

        # Replace the original format with one customized by logging level
        if record.levelno == logging.INFO:
            self._style._fmt = f"\t\t{color_codes['green']}%(msg)s{color_codes['reset']}"
        elif record.levelno == logging.ERROR:
            self._style._fmt = f"\t{color_codes['red']}ERROR: %(msg)s {color_codes['reset']}"
        elif record.levelno == logging.CRITICAL:
            self._style._fmt = f"{color_codes['blue']}%(msg)s{color_codes['reset']}"

        # Call the original formatter class to do the grunt work
        result = logging.Formatter.format(self, record)

        # Restore the original format configured by the user
        self._style._fmt = format_orig

        return result


test_logger = logging.getLogger("testing_logger")

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(MyFormatter())
test_logger.addHandler(stream_handler)

test_logger.setLevel(logging.ERROR)


def testing_func(func, tests_stuff, kwarg=None):
    test_logger.critical(f"Testing: '{func.__name__}'")
    num_tests = len(tests_stuff)
    ok_tests = 0
    for t in tests_stuff:
        input_ = t[0]
        output_ = t[1]
        kwargs = {}
        if kwarg is not None:
            kwargs = kwarg
        if len(t) == 3:
            kwargs = t[2]
        try:
            assert output_ == (value := func(input_, **kwargs))
        except AssertionError:
            test_logger.error(f"'{input_}' -> '{value}' (Expected: '{output_}')")
            continue
        test_logger.info(f"OK: {input_} -> {output_}")
        ok_tests += 1

    test_logger.critical(f"{ok_tests}/{num_tests} passed!\n\n")
