import pytest

from unit_parse import Unit, Q
from unit_parse.utils import *

example_split_list = [
    # positive control (changes)
    [["fish", "pig", "cow"], ["f", "is", "h", "pig", "cow"], {"chunks": ["is"]}],
    [["fish", Unit("g"), "cow"], ["f", "is", "h", Unit("g"), "cow"], {"chunks": ["is"]}],
    [["fishpigcow"], ["f", "i", "shpigcow"], {"chunks": ["i"]}],
    [["fishpigcow"], ["f", "i", "shpig", "c", "ow"], {"chunks": ["i", "c"]}],
    ["fish", ["f", "is", "h"], {"chunks": ["is"]}],

    # negative control (no changes)
    [["fish"], ["fish"], {"chunks": ["fish"]}],
    [["fishpigcow"], ["fishpigcow"], {"chunks": ["z"]}],
    [[Unit("g")], [Unit("g")], {"chunks": ["is"]}],
    [1, 1, {"chunks": ["is"]}],
]


@pytest.mark.parametrize("input_, output_, chunk", example_split_list)
def test_split_list(input_, output_, chunk):
    assert output_ == split_list(input_, **chunk)


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


@pytest.mark.parametrize("input_, output_, extra", test_round_off)
def test_sig_figs(input_, output_, extra):
    assert output_ == sig_figs(input_, **extra)


def test_sig_figs_error():
    with pytest.raises(TypeError):
        sig_figs("fish")


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


@pytest.mark.parametrize("input_, output_", test_list_depth)
def test_get_list_depth(input_, output_):
    assert output_ == get_list_depth(input_)


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


@pytest.mark.parametrize("input_, output_", test_remove_empty_cells)
def test_remove_empty_cells(input_, output_):
    assert output_ == remove_empty_cells(input_)


examples_quantity_difference = [
    [[Q("5 g"), Q("10 g")], Q("0.5")],

    [[5, Q("5 kg")], 1],
]


@pytest.mark.parametrize("input_, output_", examples_quantity_difference)
def test_quantity_difference(input_, output_):
    assert output_ == quantity_difference(input_[0], input_[1])


example_flatten_list = [
    [[1, 2, 3], [1, 2, 3]],
    [[[1], 2, 3], [1, 2, 3]],
    [[[1], [2, 3]], [1, 2, 3]],

    [1, 1]
]


@pytest.mark.parametrize("input_, output_", example_flatten_list)
def test_flatten_list(input_, output_):
    assert output_ == flatten_list(input_)


def test_contain_num():
    with pytest.raises(TypeError):
        contains_number(3)
