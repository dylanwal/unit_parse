import logging

from testing_func import testing_func, test_logger
from unit_parse import logger, parser, Quantity

test_logger.setLevel(logging.DEBUG)
logger.setLevel(logging.WARNING)


examples = [
    # standard examples
    ["5", Quantity("5")],
    ["5 g", Quantity("5 g")],
    ["5 g/ml", Quantity("5 g/ml")],
    ["1 K", Quantity("1 kelvin")],
    ['40 °F', Quantity("40 degF")],
    ['-40 °F', Quantity('-40 degF')],
    ['40°F', Quantity('40 degF')],
    ['20.80 mmHg', Quantity('20.80 mmHg')],
    ['20.80 mm Hg', Quantity('20.80 mmHg')],  # correcting a unit that pint gets wrong

    # scientific notation
    ["15*10**2 s", Quantity("15*10**2 s")],  # standard
    ["15*10^2 s", Quantity("15*10**2 s")],  # carrot symbol
    ["15 10**2 s", Quantity("15*10**2 s")],  # space for multiplication
    ["8.20x10**+1 ppm", Quantity("8.20*10**1 ppm")],  # x for multiplication
    ["8.20x10+1 ppm", Quantity("8.20*10**1 ppm")],  # no power symbol
    ['5e1 g/mol',  Quantity('50 g/mol')],
    ['5E1 g/mol',  Quantity('50 g/mol')],
    ['5 e1 g/mol', Quantity('50 g/mol')],
    ['5 E1 g/mol', Quantity('50 g/mol')],
    ['5e+1 g/mol', Quantity('50 g/mol')],
    ['5E-1 g/mol', Quantity('0.5 g/mol')],
    ['−66.11·10-62 ml/mol', Quantity('-66.11*10**-62 ml/mol')],
    ['−66.11·10+62 ml/mol', Quantity('-66.11*10**62 ml/mol')],
    ['−66.11·1062 ml/mol', Quantity('-66.11*10**62 ml/mol')],

    # messed up units/ units with powers
    ["2.3 gcm", Quantity("2.3 g*cm")],
    ["2.3 gcm**3", Quantity("2.3 g*cm**3")],
    ["2.3 gcm**3", Quantity("2.3 g*cm^3")],
    ["2.3     g", Quantity("2.3 g")],
    ["2.3 mlgcm", Quantity("2.3 ml*g*cm")],
    ['42.3 gcm-3', Quantity('42.3 g*cm**-3')],
    ['42.3 g cm-3', Quantity('42.3 g*cm**-3')],
    ['−66.11·10-62 cm3/mol', Quantity('-66.11*10**-62 cm**3/mol')],
    ['−66.11·10+62 cm3/mol', Quantity('-66.11*10**62 cm**3/mol')],
    ['−66.11·1062 cm3/mol', Quantity('-66.11*10**62 cm**3/mol')],

    # parenthesis (brackets turned to parenthesis)
    ["(4.0 °C)", Quantity("4 degC")],
    ["[4.0 °C]", Quantity("4 degC")],
    ["4.0 (°C)", Quantity("4 degC")],
    ["4.0 (°C))", Quantity("4 degC")],
    [")4.0 (°C)", Quantity("4 degC")],
    ["(4.0 (°C)", Quantity("4 degC")],
    ["()4.0 (°C)", Quantity("4 degC")],
    ['4.0 °C [39.2 g/[mol * s]]', [Quantity("4 degC"), Quantity("39.2 g/(mol * s)")]],

    # conditions
    ["37.34 kJ/mole (at 25 °C)", [Quantity("37.34 kJ/mole"), Quantity("25 degC")]],
    ['20.8 mm Hg @ 25 °C', [Quantity('20.8 mmHg'), Quantity('25 degC')]],
    ['20.8 mm Hg (25 °C)', [Quantity('20.8 mmHg'), Quantity('25 degC')]],
    ['20.8 mm Hg at 25 °C', [Quantity('20.8 mmHg'), Quantity('25 degC')]],

    # list of quantities
    ['18 mm Hg; 20 mm Hg', [Quantity('18 mmHg'), Quantity('20 mmHg')]],
    ['18 mm Hg; 20 mm Hg', [Quantity('18 mmHg'), Quantity('20 mmHg')]],
    ['18 mm Hg @ 68 °F; 20 mm Hg @ 77° F',
     [[Quantity('18 mmHg'), Quantity('68 degF')], [Quantity('20 mmHg'), Quantity('77 degF')]]],
    ['18 mm Hg @ 68 °F ; 20 mm Hg @ 77° F (NTP, 1992)',
     [[Quantity('18 mmHg'), Quantity('68 degF')], [Quantity('20 mmHg'), Quantity('77 degF')]]],
    ['18 mm Hg at 68 °F ; 20 mm Hg at 77 °F',
     [[Quantity('18 mmHg'), Quantity('68 degF')], [Quantity('20 mmHg'), Quantity('77 degF')]]],

    # ranges
    ['115.2-115.3 °C', Quantity('115.2 degC')],
    ['115.2 - 115.3 °C', Quantity('115.2 degC')],

    # words
    ["8.20x10+1 ppm; pure", Quantity("8.20*10**1 ppm")],
    ['40 °F (NTP, 1992)', Quantity("40 degF")],
    ['4.0 °C (39.2 °F) - closed cup', Quantity("4 degC")],
    ['4.0 °C [39.2 g/[mol * s]] - closed cup', [Quantity("4 degC"), Quantity("39.2 g/(mol * s)")]],
    ['4.0 °C [39.2 g/[mol * s] approx.] - closed cup', [Quantity("4 degC"), Quantity("39.2 g/(mol * s)")]],
    ['4.0 °C [39.2g/[mol*s] approx.] - closed cup', [Quantity("4 degC"), Quantity("39.2 g/(mol * s)")]],
    ['4.0 °C [39.2g/[mol*s]approx.] - closed cup', [Quantity("4 degC"), Quantity("39.2 g/(mol * s)")]],

    # duplicates of same quantity different units
    ["4.0 °C (39.2 °F)", Quantity("4 degC")],
    ['-14.390 BTU/LB= -7992 CAL/G= -334.6X10+5 J/KG', Quantity('-14.390 BTU/lb')],

    # complex
    ['18 mm Hg at 68 °F ; 20 mm Hg at 77° F (NTP, 1992)', [[Quantity('18 mmHg'), Quantity('68 degF')],
                                                           [Quantity('20 mmHg'), Quantity('77 degF')]]],
    ['Sound travels at 0.34 km/s', Quantity('0.34 km/s')],
    ['Pass me a 300 ml beer.', Quantity("300 ml")],


    # stuff it gets wrong
    ['Index of refraction: 1.50920 @ 20 °C/D', [Quantity('1.50920'), Quantity('20 degC')]],
    ['Vapor pressure, kPa at 20 °C: 2.0', [Quantity('2.0 kPa'), Quantity('20 degC')]],

]

delete_text = [
    "approx.",
    "approximate",
    "approx",
    "closed cup",
    "(NTP, 1992)",
    ]


def pre_process_values():
    for example in examples:
        result = parser(example[0])
        print(f"{example[0]} --> {result}")


def testing():
    testing_func(parser, examples, {"remove_string": delete_text})


if __name__ == '__main__':
    testing()
