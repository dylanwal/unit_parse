import logging

from testing_func import testing_func, test_logger
from unit_parse import logger, Quantity, reduce_quantities

test_logger.setLevel(logging.DEBUG)
logger.setLevel(logging.INFO)

examples = [  # [Input, Output]
    # positive control (works, does changes)
    [[Quantity("-44 degree_Fahrenheit"), Quantity("-41.6 degree_Celsius"), Quantity("-42 degree_Celsius")],
     Quantity("-44 degF")],

    [[Quantity("-45 degree_Celsius"), Quantity("-41.6 degree_Celsius"), Quantity("-42 degree_Celsius"),
      Quantity("-40 degree_Celsius"), Quantity("-70 degree_Celsius")],
     Quantity("-44 degF")],

    [[Quantity("68 degree_Fahrenheit"), Quantity("68.0 degree_Fahrenheit"), Quantity("20.0 degree_Celsius"),
      Quantity("293.15 kelvin * speed_of_light ** 2")],
     Quantity("68 degF")],

    [[Quantity("20.8 millimeter_Hg"), Quantity("2.0 dimensionless"), Quantity("16 millimeter_Hg"),
      [
          [Quantity("18 millimeter_Hg"), Quantity("68 degree_Fahrenheit")],
          [Quantity("20 millimeter_Hg"), Quantity("77.0 degree_Fahrenheit")]
      ],
      [Quantity("20.8 millimeter_Hg"), Quantity("25 degree_Celsius")]
      ],
     [
         [Quantity("18 millimeter_Hg"), Quantity("68 degree_Fahrenheit")],
         [Quantity("20 millimeter_Hg"), Quantity("77.0 degree_Fahrenheit")]
     ]],

    [[
        [Quantity("68 degree_Fahrenheit"), Quantity("760.0 millimeter_Hg")],
        Quantity("68.0 degree_Fahrenheit"),
        Quantity("20.0 degree_Celsius"),
        Quantity("293.15 kelvin * speed_of_light ** 2"),
        Quantity("68 degree_Fahrenheit"),
        Quantity("68 degree_Fahrenheit")
    ], [Quantity("68 degree_Fahrenheit"), Quantity("760.0 millimeter_Hg")]],

    [[0.65, Quantity('0.65 dimensionless'), Quantity('0.65 dimensionless')], Quantity('0.65 dimensionless')]

    # negative control (fails/ does no changes)

]

testing_func(reduce_quantities, examples)
