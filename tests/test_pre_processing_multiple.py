import pytest

from unit_parse.pre_processing_multiple import *

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


@pytest.mark.parametrize("input_, output_", examples)
def test_reduce_parenthesis(input_, output_):
    assert output_ == reduce_parenthesis(input_)


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


@pytest.mark.parametrize("input_, output_", test_condition_finder)
def test_condition_finder(input_, output_):
    assert output_ == condition_finder(input_)


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


@pytest.mark.parametrize("input_, output_", test_multiple_quantities)
def test_multiple_quantities(input_, output_):
    assert output_ == multiple_quantities(input_, sep=[";"])
