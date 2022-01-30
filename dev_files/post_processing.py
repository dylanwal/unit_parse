import logging

from testing_func import testing_func, test_logger
from unit_parse.post_processing import *
from unit_parse import logger

test_logger.setLevel(logging.DEBUG)
logger.setLevel(logging.CRITICAL)

test_remove_duplicates = [  # [Input, Output]
    # positive control (changes)
    [[Quantity("40 degF"), Quantity("4 degC")], [Quantity("40 degF")]],
    [[Quantity("40 degF"), Quantity("4 degC"), Quantity("32 degF"), Quantity("0 degC")],
     [Quantity("40 degF"), Quantity("32 degF")]],
    [[[Quantity("13.565 kcal/mol"), Quantity("25 °C")], [Quantity("10.60 kcal/mol")]],
     [[Quantity("13.565 kcal/mol"), Quantity("25 °C")]]],
    [[[Quantity("13.565 kcal/mol"), Quantity("25 °C")], Quantity("10.60 kcal/mol")],
     [[Quantity("13.565 kcal/mol"), Quantity("25 °C")]]],

    # negative control (no changes)
    [[Quantity("40 degF")], [Quantity("40 degF")]],
    [Quantity("40 degF"), Quantity("40 degF")],
    [[[Quantity("40 degF"), Quantity("20 kPa")]], [[Quantity("40 degF"), Quantity("20 kPa")]]],
    [[[Quantity("40 degF"), Quantity("4 degF")]], [[Quantity("40 degF"), Quantity("4 degF")]]],

]
testing_func(remove_duplicates, test_remove_duplicates)
