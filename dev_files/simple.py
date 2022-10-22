import logging

from unit_parse import parser, logger

logger.setLevel(logging.DEBUG)

result = parser("3.6E+00004 mg/L")
print(result)

