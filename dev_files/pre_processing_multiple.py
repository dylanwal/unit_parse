import logging

from testing_func import testing_func, test_logger
from unit_parse.pre_processing_multiple import *
from unit_parse import logger

test_logger.setLevel(logging.DEBUG)
logger.setLevel(logging.CRITICAL)

examples = [  # [Input, Output]
    # positive control (works)
    ["(aaaaa)", ["aaaaa"]],
    ["(aa(a)aa)", ["aa", "a", "aa"]],
    ["(aaa)(aa)", ["aaa", "aa"]],
    ["aaa(aa)", ["aaa", "aa"]],
    ["a(aa(aa))", ["a", "aa", "aa"]],
    ["(60 m/(s*ml))", ["60 m/(s*ml)"]],
    ["5 g/(ml) (60 m/(s*ml))", ["5 g/(ml)", "60 m/(s*ml)"]],

    ["(aaaaa))", ["aaaaa"]],
    ["(aaaaa", ["aaaaa"]],
    ["((aaaaa", ["aaaaa"]],
    ["aa))aaa", ["aa", "aaa"]],
    [")aaaaa(", ["aaaaa"]],
    ["aaa)(aa", ["aaa", "aa"]],
    ["(aa(aaa)", ["aa", "aaa"]],

    # negative control (fails)
]
testing_func(reduce_parenthesis, examples)


test_condition_finder = [  # [Input, Output]
    # # positive control (works)
    ['18 mm Hg @ 68 °F ', ['18 mm Hg', '68 °F']],
    ['20 mm Hg @ 77° F', ['20 mm Hg', '77° F']],
    [' 20 mm Hg @ 77° F (NTP, 1992)', ['20 mm Hg', '77° F', 'NTP, 1992']],

    ['40 °F (4 °C) (Closed cup)', ['40 °F', '4 °C', 'Closed cup']],
    ['40 °F (4 °C)', ['40 °F', '4 °C']],
    ['40 °F (Closed cup)', ['40 °F', 'Closed cup']],
    ['40 °F(Closed cup)', ['40 °F', 'Closed cup']],
    ['40 °F ((4 °C) Closed cup)', ['40 °F', '4 °C', 'Closed cup']],
    ['((4 °C) Closed cup)', ['4 °C', 'Closed cup']],
    ['(4 °C Closed cup)', ['4 °C Closed cup']],

    # negative control (fails)
    ['20.8 mm Hg 25 °C', ['20.8 mm Hg 25 °C']],
    ['20.8 mm Hgat25 °C', ['20.8 mm Hgat25 °C']],
    ['Pass me a 300 ml beer.', ['Pass me a 300 ml beer.']],
    ["42.3 gcm-3", ["42.3 gcm-3"]],
    ["40 °F", ["40 °F"]],
    ["39.2 g/[mol * s]]", ["39.2 g/[mol * s]]"]],
    ['−66.11·10-62 cm3/mol', ['−66.11·10-62 cm3/mol']],
    ['40 g/(mol s)', ['40 g/(mol s)']],
]
testing_func(condition_finder, test_condition_finder)


test_multiple_quantities = [  # [Input, Output]
    # positive control (works)
    ['18 mm Hg at 68 °F ; 20 mm Hg at 77° F', ['18 mm Hg at 68 °F', '20 mm Hg at 77° F']],
    ['18 mm Hg @ 68 °F ; 20 mm Hg @ 77° F (NTP, 1992)', ['18 mm Hg @ 68 °F', '20 mm Hg @ 77° F (NTP, 1992)']],

    # negative control (fails)
    ['20.8 mm Hg @ 25 °C', ['20.8 mm Hg @ 25 °C']],
    ['20.8 mm Hgat25 °C', ['20.8 mm Hgat25 °C']],
    ['Pass me a 300 ml beer.', ['Pass me a 300 ml beer.']],
    ["42.3 gcm-3", ["42.3 gcm-3"]],
    ["40 °F", ["40 °F"]],
    ["39.2 g/[mol * s]]", ["39.2 g/[mol * s]]"]],
    ['−66.11·10-62 cm3/mol', ['−66.11·10-62 cm3/mol']]
]

testing_func(multiple_quantities, test_multiple_quantities, {"sep": [";"]})
