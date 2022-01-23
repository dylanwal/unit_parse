import logging

from testing_func import testing_func, test_logger
from unit_parse import logger, Unit
from unit_parse import *

test_logger.setLevel(logging.DEBUG)
logger.setLevel(logging.DEBUG)


result = parser('4.0 °C (39.2 °F) - closed cup')

print(result)
print("hi")
