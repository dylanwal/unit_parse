import logging

from testing_func import testing_func, test_logger
from unit_parse import logger, Q, U, reduce_quantities

test_logger.setLevel(logging.DEBUG)
logger.setLevel(logging.WARNING)

examples = [  # [Input, Output]
    # positive control (works, does changes)
    [[[[0.633, Q('68 degF')]], [[0.6709, Q('0.0')]], [[Q('40.89 pound / foot ** 3'), Q('35 degC')]],
      [[Q('0.2991 pound / foot ** 3'), Q('70 degC')]], Q('0.6'), 0.667, [[0.633, '68 degF']], 2.09],
     [[Q('40.89 pound / foot ** 3'), Q('35 degC')]]],

    [[Q("2 ppm"), Q("5 mol/ml"), Q("10 mol/cm**3")], Q("2 ppm"), {"prefer_unit": U("ppm")}],

    [[Q('0.01 m ** 3 * atm / mole'), [[Q('0.00664 m ** 3 * atm / mole'), Q('25 degC')]]],
     [[Q('0.00664 m ** 3 * atm / mole'), Q('25 degree_Celsius')]]],

    [[[[Q('18 mmHg'), Q('68 degF')], [Q('20 mm_Hg'), Q('77 degF')]], Q('20.8 mmHg'), [[Q('20.8 mmHg'), Q('25 degC')]],
      Q('2.0'), Q('16 mmHg'), Q('16 mmHg')],
     [[Q('18 mmHg'), Q('68 degF')], [Q('20 mm_Hg'), Q('77 degF')]]],

    [[[[0.983, Q('68 degF')]], [[0.98272, Q('20.0')]], Q('0.98'), [[0.983, Q('68')]], Q('0.98')],
     [[0.983, Q('68 degF')]]],

    [[[[0.983, Q('68 degF')]], [[0.98272, Q('20.0')]], Q('0.98 g/cm**3'), [[0.983, Q('68')]], Q('0.98')],
     Q('0.98 g/cm**3')],

    [[-3.17, Q('-3.17')], Q('-3.17')],

    [[[[Q('1 millimeter_Hg'), Q('225 degree_Fahrenheit')]], Q('0.000118 millimeter_Hg'),
      [[Q('0.000118 millimeter_Hg'), Q('25 degree_Celsius')]]],
     [[Q('1 millimeter_Hg'), Q('225 degF')]]],

    [[[[1.056, Q('68 degF')]], Q('1.056 dimensionless'), Q('1.06 gram / centimeter ** 3')],
     Q('1.06 gram / centimeter ** 3')],

    [[Q("-44 degF"), Q("-41.6 degC"), Q("-42 degC")],
     Q("-44 degF")],

    [[Q("-45 degC"), Q("-41.6 degC"), Q("-42 degC"), Q("-40 degC"), Q("-70 degC")],
     Q("-44 degF")],

    [[Q("68 degF"), Q("68.0 degF"), Q("20.0 degC"), Q("293.15 kelvin * speed_of_light ** 2")],
     Q("68 degF")],

    [[Q("20.8 mmHg"), Q("2.0 dimensionless"), Q("16 mmHg"),
      [[Q("18 mmHg"), Q("68 degF")], [Q("20 mmHg"), Q("77.0 degF")]], [Q("20.8 mmHg"), Q("25 degC")]],
     [[Q("18 mmHg"), Q("68 degF")], [Q("20 mmHg"), Q("77.0 degF")]]],

    [[[Q("68 degF"), Q("760.0 mmHg")], Q("68.0 degF"), Q("20.0 degC"), Q("293.15 kelvin * speed_of_light ** 2"),
      Q("68 degF"), Q("68 degF")],
     [Q("68 degF"), Q("760.0 mmHg")]],

    [[0.65, Q('0.66'), Q('0.65'), Q('0.65')], Q('0.65')],

    [[[0.65, Q('25  degC')], Q('0.65'), Q('0.65')], [0.65, Q('25  degC')]],

    [[[Q('50  kg'), Q('25  degC')], Q('0.65 dimensionless'), Q('0.65 dimensionless')],
     [Q('50  kg'), Q('25  degC')]]

    # negative control (fails/ does no changes)

]

testing_func(reduce_quantities, examples)
