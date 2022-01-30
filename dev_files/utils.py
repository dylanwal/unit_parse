import logging

from testing_func import testing_func, test_logger
from unit_parse import logger, Unit, Q
from unit_parse.utils import *

test_logger.setLevel(logging.DEBUG)
logger.setLevel(logging.DEBUG)


test_split_list = [
    # positive control (changes)
    [["fish","pig", "cow"], ["f", "is", "h", "pig", "cow"], {"chunks": ["is"]}],
    [["fish", Unit("g"), "cow"], ["f", "is", "h", Unit("g"), "cow"], {"chunks": ["is"]}],
    [["fishpigcow"], ["f", "i", "shpigcow"], {"chunks": ["i"]}],
    [["fishpigcow"], ["f", "i", "shpig", "c", "ow"], {"chunks": ["i", "c"]}],

    # negative control (no changes)
    [["fish"], ["fish"], {"chunks": ["fish"]}],
    [["fishpigcow"], ["fishpigcow"], {"chunks": ["z"]}],
    [[Unit("g")], [Unit("g")], {"chunks": ["is"]}],
]
testing_func(split_list, test_split_list)


test_round_off = [  # [Input, Output]
    # positive control (works)
    [234.2342300000001, 234.23423, {"sig_digit": 15}],
    [234.2342399999999999, 234.23424, {"sig_digit": 15}],
    [234.2342300000001, 234.23, {"sig_digit": 5}],
    [234.2342399999999999, 234.23, {"sig_digit": 5}],
    [234.2342399999999999, 200, {"sig_digit": 1}],
    [-234.2342399999999999, -200, {"sig_digit": 1}],
    [-234.2342399999999999, -234.23424, {"sig_digit": 15}],
    # negative control (fails)

]
testing_func(sig_figs, test_round_off)


test_list_depth = [  # [Input, Output]
    # positive control (works)
    ["", 0],
    [[], 0],
    ["asds", 0],
    [1, 0],
    [["aaa"], 1],
    [[["aaa"]], 2],
    [[["aaa", "aaa", "aaa"], ["aaa"], ["aaa"]], 2],
    [[["aaa", "aaa", "aaa"], ["aaa"], ["aaa"]], 2],
    [[[["aaa"], ["aaa"], ["aaa"]]], 3],

    # negative control (fails)

]
testing_func(get_list_depth, test_list_depth)


test_remove_empty_cells = [  # [Input, Output]
    # positive control (works)
    [[], None],
    [[""], None],
    [["asds"], ["asds"]],
    [1, 1],
    [["aaa", ""], ["aaa"]],
    [["aaa", []], ["aaa"]],
    [[["aaa", []]], [["aaa"]]],
    [[["aaa", [""]]], [["aaa"]]],

    # negative control (fails)

]
testing_func(remove_empty_cells, test_remove_empty_cells)


examples_quantity_difference = [
    [Q("5 g"), Q("0.5"), {"quantity2": Q("10 g")}],

    [5, 1, {"quantity2": Q("10 g")}],
]
testing_func(quantity_difference, examples_quantity_difference)

