import logging

from testing_func import testing_func, test_logger
from unit_parse.pre_processing_substitution import *
from unit_parse import logger, config

test_logger.setLevel(logging.DEBUG)
logger.setLevel(logging.CRITICAL)


test_reduce_ranges = [  # [Input, Output]
    # positive control (makes changes)
    ['115.2-115.3 °C', '115.2 °C'],
    ['115.2 - 115.3 °C', '115.2 °C'],
    ["	0.909 g/cm3", "0.909 g/cm3"],

    # negative control (no changes made)
    ["66.11·10**-62 cm-3/mol", "66.11·10**-62 cm-3/mol"],
    ['-14.390 BTU/LB= -7992 CAL/G= -334.6*10**5 J/KG', '-14.390 BTU/LB= -7992 CAL/G= -334.6*10**5 J/KG'],
    ["42.3 gcm-3", "42.3 gcm-3"],
    ["0.909 g/cm3", "0.909 g/cm3"],
    ["40 °F", "40 °F"],
    ["39.2 g/[mol * s]]", "39.2 g/[mol * s]]"],
]
testing_func(reduce_ranges, test_reduce_ranges)


test_remove_words = [  # [Input, Output]
    # positive control (makes changes)
    ['Detection in water 0.73 ppm; Chemically pure', '0.73 ppm;'],
    ['Odor Threshold Range 0.15 to 25 ppm', '0.15 to 25 ppm'],
    ["4.0 °C [39.2 g/[mol * s]] - closed cup", "4.0 °C [39.2 g/[mol * s]] - cup"],
    ["Index of refraction: 1.50920 @ 20 °C/D", "1.50920 @ 20 °C/D"],
    ["Vapor pressure, kPa at 20 °C: 2.0", "kPa at 20 °C: 2.0"],

    # negative control (no changes made)
    ["5 cups", "5 cups"],
    ["3e-10 pascal", "3e-10 pascal"],
    ["332.34 kelvin", "332.34 kelvin"],

]
testing_func(remove_words, test_remove_words, {"words": config.english_dict})


test_sci_notation = [  # [Input, Output]
    # positive control (makes changes)
    ["66.11·10-62 cm3/mol", "66.11·10**-62 cm3/mol"],
    ["66.11·10-62 cm-3/mol", "66.11·10**-62 cm-3/mol"],
    ["15 10**2 s", "15*10**2 s"],
    ['-14.390 BTU/LB= -7992 CAL/G= -334.6*10**5 J/KG', '-14.390 BTU/LB= -7992 CAL/G= -334.6*10**5 J/KG'],
    ["	0.909 g/cm3", "0.909 g/cm3"],
    ['5.3e1 g/mol', '5.3*10**1 g/mol'],
    ['5.3E1 g/mol', '5.3*10**1 g/mol'],

    # negative control (no changes made)
    ['5.3*10**1 g/mol', '5.3*10**1 g/mol'],
    ["42.3 gcm-3", "42.3 gcm-3"],
    ["0.909 g/cm3", "0.909 g/cm3"],
    ["40 °F", "40 °F"],
    ["39.2 g/[mol * s]]", "39.2 g/[mol * s]]"],
]

testing_func(sub_sci_notation, test_sci_notation)


test_power = [  # [Input, Output]
    # positive control (makes changes)
    ["42.3 gcm-3", "42.3 gcm**-3"],
    ["66.11·10-62 cm3/mol", "66.11·10-62 cm**3/mol"],
    ["66.11·10-62 cm-3/mol", "66.11·10-62 cm**-3/mol"],
    ["	0.909 g/cm3", "0.909 g/cm**3"],

    # negative control (no changes made)
    ["40 °F", "40 °F"],
    ["39.2 g/[mol * s]]", "39.2 g/[mol * s]]"],
    ['-14.390 BTU/LB= -7992 CAL/G= -334.6*10+5 J/KG', '-14.390 BTU/LB= -7992 CAL/G= -334.6*10+5 J/KG']
]

testing_func(sub_power, test_power)


test_sub_pattern1 = [
    # positive control (makes changes)
    ['Pass me a 300 ml beer.', '300 ml beer.'],
    ["	0.909 g/cm3", "0.909 g/cm3"],
    ['Sound travels at 0.34 km/s', '0.34 km/s'],

    # negative control (no changes made)
    ["42.3 gcm-3", "42.3 gcm-3"],
    ["40 °F", "40 °F"],
    ["39.2 g/[mol * s]]", "39.2 g/[mol * s]]"],
    ['−66.11·10-62 cm3/mol', '−66.11·10-62 cm3/mol']
]

pattern = ["^[a-zA-Z;,.: /]*", ""]
testing_func(sub_general, test_sub_pattern1, {"patterns": [pattern]})


test_sub_pattern2 = [
    # positive control (makes changes)
    ["37.34 kJ/mole (at 25 °C)", "37.34 kJ/mole ( @ 25 °C)"],
    ['20.8 mm Hg at 25 °C', '20.8 mm Hg  @ 25 °C'],
    ["	0.909 g/cm3", "0.909 g/cm3"],
    ['Sound travels at 0.34 km/s', 'Sound travels  @ 0.34 km/s'],

    # negative control (no changes made)
    ['20.8 mm Hg @ 25 °C', '20.8 mm Hg @ 25 °C'],
    ['20.8 mm Hgat25 °C', '20.8 mm Hgat25 °C'],
    ['Pass me a 300 ml beer.', 'Pass me a 300 ml beer.'],
    ["42.3 gcm-3", "42.3 gcm-3"],
    ["40 °F", "40 °F"],
    ["39.2 g/[mol * s]]", "39.2 g/[mol * s]]"],
    ['−66.11·10-62 cm3/mol', '−66.11·10-62 cm3/mol']
]

pattern = ["(?<=[^a-zA-Z])at([^a-zA-Z])", " @ "]
testing_func(sub_general, test_sub_pattern2, {"patterns": [pattern]})


test_sub_pattern3 = [
    # positive control (makes changes)
    ['-14.390 BTU/LB= -7992 CAL/G= -334.6X10+5 J/KG', '-14.390 BTU/LB'],
    ["	0.909 g/cm3", "0.909 g/cm3"],

    # negative control (no changes made)
    ['Sound travels at 0.34 km/s', 'Sound travels at 0.34 km/s'],
    ['20.8 mm Hg @ 25 °C', '20.8 mm Hg @ 25 °C'],
    ['20.8 mm Hgat25 °C', '20.8 mm Hgat25 °C'],
    ['Pass me a 300 ml beer.', 'Pass me a 300 ml beer.'],
    ["42.3 gcm-3", "42.3 gcm-3"],
    ["40 °F", "40 °F"],
    ["39.2 g/[mol * s]]", "39.2 g/[mol * s]]"],
    ['−66.11·10-62 cm3/mol', '−66.11·10-62 cm3/mol']
]

pattern = ["={1}.*$", ""]
testing_func(sub_general, test_sub_pattern3, {"patterns": [pattern]})


test_sub_pattern3 = [
    # positive control (makes changes)
    ['Sound travels: 0.34 km/s', '0.34 km/s'],

    # negative control (no changes made)
    ['Sound travels at 0.34 km/s', 'Sound travels at 0.34 km/s'],
    ['20.8 mm Hg @ 25 °C', '20.8 mm Hg @ 25 °C'],
    ['20.8 mm Hgat25 °C', '20.8 mm Hgat25 °C'],
    ['Pass me a 300 ml beer.', 'Pass me a 300 ml beer.'],
    ["42.3 gcm-3", "42.3 gcm-3"],
    ["40 °F", "40 °F"],
    ["39.2 g/[mol * s]]", "39.2 g/[mol * s]]"],
    ['−66.11·10-62 cm3/mol', '−66.11·10-62 cm3/mol'],
]

pattern = ["^.*:{1}", ""]
testing_func(sub_general, test_sub_pattern3, {"patterns": [pattern]})
