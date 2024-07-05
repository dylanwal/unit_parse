import logging

from unit_parse import parser, logger

logger.setLevel(logging.DEBUG)

result = parser("Between 10 and 20 ºC")
# answer = parser("3.6*10**4 mg/L")
print(result)
# print(answer)
# print(result == answer)

