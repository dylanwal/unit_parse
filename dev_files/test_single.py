import logging

from testing_func import testing_func, test_logger
from unit_parse import logger, Unit
from unit_parse import *

# test_logger.setLevel(logging.DEBUG)
logger.setLevel(logging.DEBUG)

result = parser("37.34 kJ/mole (at 25 °C)")

print(result)

