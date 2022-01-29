import pytest

from unit_parse.post_processing import *


test_remove_duplicates = [  # [Input, Output]
    # positive control (changes)
    [[Quantity("40 degF"), Quantity("4 degC")], [Quantity("40 degF")]],
    [[Quantity("40 degF"), Quantity("4 degC"), Quantity("32 degF"), Quantity("0 degC")],
     [Quantity("40 degF"), Quantity("32 degF")]],

    # negative control (no changes)
    [[Quantity("40 degF")], [Quantity("40 degF")]],
    [Quantity("40 degF"), Quantity("40 degF")],
    [[Quantity("40 degF"), Quantity("20 kPa")], [Quantity("40 degF"), Quantity("20 kPa")]],
    [[Quantity("40 degF"), Quantity("4 degF")], [Quantity("40 degF"), Quantity("4 degF")]],

]


@pytest.mark.parametrize("input_, output_", test_remove_duplicates)
def test_remove_duplicates(input_, output_):
    assert output_ == remove_duplicates(input_)
