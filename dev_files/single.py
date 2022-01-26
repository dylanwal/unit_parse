import logging

from testing_func import testing_func, test_logger
from unit_parse import logger, Unit, parser
from unit_parse.pre_processing_substitution import *

test_logger.setLevel(logging.DEBUG)
logger.setLevel(logging.DEBUG)

# test_remove_words = [  # [Input, Output]
#     # positive control (makes changes)
#     # ['Detection in water 0.73 ppm; Chemically pure', '0.73 ppm;'],
#     ['Odor Threshold Range 0.15 to 25 ppm', '0.15 to 25 ppm'],
#     ["4.0 °C [39.2 g/[mol * s]] - closed cup", "4.0 °C [39.2 g/[mol * s]] - cup"],
#     ["Index of refraction: 1.50920 @ 20 °C/D", "1.50920 @ 20 °C/D"],
#     ["Vapor pressure, kPa at 20 °C: 2.0", "kPa at 20 °C: 2.0"],
#
#     # negative control (no changes made)
#     ["5 cups", "5 cups"],
#     ["3e-10 pascal", "3e-10 pascal"],
#     ["332.34 kelvin", "332.34 kelvin"],
#
# ]
# testing_func(remove_words, test_remove_words, {"words": config.english_dict})

result = parser("1.0722 at 68 °F (EPA, 1998)")

print(result)


