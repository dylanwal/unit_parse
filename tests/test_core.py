import pytest

from unit_parse.core import Quantity, Unit
from unit_parse.core import frame_shift
from unit_parse.core import get_quantity, get_unit, get_value
from unit_parse.core import last_minute_sub, merge_split_text
from unit_parse.core import split_on_division_symbol, split_on_multiplication_symbol, split_on_powers

test_get_value = [  # [Input, Output]
    # positive control (works)
    ["42.3 gcm-3", (42.3, '42.3')],
    ["42.3gcm-3", (42.3, '42.3')],
    ["66.11*10**-62 g", (6.611e-61, '66.11*10**-62')],
    ["66.11*10**62 cm-3/mol", (6.611e+63, '66.11*10**62')],
    ["0.909 g/cm3", (0.909, '0.909')],
    ["-0.909 g/cm3", (-0.909, '-0.909')],
    ["  -0.909 g/cm3", (-0.909, '-0.909')],
    ["0.343", (0.343, '0.343')],

    # negative control (fails)
    ["c40 °F", (None, "")],
    ["", (None, "")],
    ["*", (None, "")],
    ["*34gd", (None, "")],
]


@pytest.mark.parametrize("input_, output_", test_get_value)
def test_get_value(input_, output_):
    assert output_ == get_value(input_)


test_units_with_powers = [
    # positive control (changes)
    ["g**2cm**-3", [Unit("g**2"), Unit("cm**-3")]],
    ["g**2 cm**-3", [Unit("g**2"), Unit("cm**-3")]],
    ["g*cm**-3", ["g*", Unit("cm**-3")]],
    ["g*cm**-35", ["g*", Unit("cm**-35")]],
    ["g cm**-35", ["g ", Unit("cm**-35")]],
    ['cm**3/mol', [Unit('cm**3'), '/mol']],
    [[""], []],

    # negative control (no changes)
    ["gcm**-3", ["gcm**-3"]],
    [["g/(mol * s)"], ["g/(mol * s)"]],
    ["° F NTP, 1992", ["° F NTP, 1992"]],
    [["° F NTP, 1992"], ["° F NTP, 1992"]],

]


@pytest.mark.parametrize("input_, output_", test_units_with_powers)
def test_split_on_powers(input_, output_):
    assert output_ == split_on_powers(input_)


test_units_with_multi = [
    # positive control (changes)
    ["g*cm", [Unit("g"), Unit("cm")]],
    ["g*cm**-3", [Unit("g"), Unit("cm**-3")]],
    ["g*", [Unit("g")]],
    ["g*ml*cm", [Unit("g"), Unit("ml*cm")]],
    [["g*", Unit("cm**-3")], [Unit("g"), Unit("cm**-3")]],
    [["gml*"], ["gml"]],

    # negative control (no changes)
    [[Unit("g"), Unit("cm**-3")], [Unit("g"), Unit("cm**-3")]],
    [["g", Unit("cm**-3")], ["g", Unit("cm**-3")]],
    ["gcm**-3", ["gcm**-3"]],
    ["g cm**-35", ["g cm**-35"]],
    [[""], [""]],
]


@pytest.mark.parametrize("input_, output_", test_units_with_multi)
def test_split_on_multiplication_symbol(input_, output_):
    assert output_ == split_on_multiplication_symbol(input_)


test_units_with_div = [
    # positive control (changes)
    ["g/ml", [Unit("g"), "/", Unit("ml")]],
    ["g /ml", [Unit("g"), "/", Unit("ml")]],
    ["g/ ml", [Unit("g"), "/", Unit("ml")]],
    ["g / ml", [Unit("g"), "/", Unit("ml")]],
    ["g/", [Unit("g"), "/"]],
    ["/g", ["/", Unit("g")]],
    ["gmol/s", ["gmol", "/", Unit("s")]],
    ["g/mol/s", [Unit("g"), "/", Unit("mol"), "/", Unit("s")]],
    [["gmol/s", Unit("cm**-3")], ["gmol", "/", Unit("s"), Unit("cm**-3")]],

    # negative control (no changes)
    [[""], []],
]


@pytest.mark.parametrize("input_, output_", test_units_with_div)
def test_split_on_division_symbol(input_, output_):
    assert output_ == split_on_division_symbol(input_)


test_merge_split_text = [
    # positive control (changes)
    [[Unit("g**2"), Unit("cm**-3")], Unit("g**2 * cm**-3")],
    [[Unit("g**2"), "/", Unit("cm**-3")], Unit("g**2 / cm**-3")],
    [[Unit("g**2"), "/", Unit("cm"), "/", Unit("s")], Unit("g**2/cm/s")],

    # negative control (no changes)

]


@pytest.mark.parametrize("input_, output_", test_merge_split_text)
def test_merge_split_text(input_, output_):
    assert output_ == merge_split_text(input_)


test_frame_shift = [  # [Input, Output]
    # positive control (works)
    ["gcm", Unit("g*cm")],
    ["gcm**3", Unit("g*cm**3")],
    [" g", Unit("g")],
    ["mlgcm", Unit("ml*g*cm")],

    # negative control (fails)
    ["- closed cup", None],
    ["c40 °F", None],
    ["", None],
    ["*", None],
    ["*34gd", None],
]


@pytest.mark.parametrize("input_, output_", test_frame_shift)
def test_frame_shift(input_, output_):
    assert output_ == frame_shift(input_)


test_get_unit = [  # [Input, Output]
    # positive control (works)
    # ['°C - closed', Unit("degC")],
    # [' °F', Unit('degF')],
    # ['°F', Unit("degF")],
    ["g*cm**-3", Unit("g*cm**-3")],
    ['cm**3/mol', Unit('cm**3/mol')],
    ['g/mol', Unit('g/mol')],
    ["gcm**-3", Unit("g*cm**-3")],
    ["g cm**-3", Unit("g*cm**-3")],
    ['ml beer.', Unit("ml")],
    ["c40 °F", Unit("degF")],

    # negative control (fails)
    ["*", None],
    [' ', None],
    ["*34gd", None],
    [None, None]
]


@pytest.mark.parametrize("input_, output_", test_get_unit)
def test_get_unit(input_, output_):
    assert output_ == get_unit(input_)


test_to_quantity = [  # [Input, Output]
    # # positive control (works)
    ['40 °F ', Quantity("40 degF")],
    ['40°F', Quantity('40 degF')],
    ["42.3 g*cm**-3", Quantity("42.3 g*cm**-3")],
    ['4.0 °C', Quantity("4 degC")],
    [' 4.0 °C', Quantity("4 degC")],
    ['4.0', Quantity("4")],
    ['-66.11*10**-62 cm**3/mol', Quantity('-66.11*10**-62 cm**3/mol')],
    ['-66.11*10**+62 cm**3/mol', Quantity('-66.11*10**62 cm**3/mol')],
    ['10e1 g/mol', Quantity('10e1 g/mol')],
    ['4.0 °C (39.2g/(mol*s)approx.) - closed cup', Quantity("4* degC")],
    ['300 ml beer.', Quantity("300 ml")],
    #
    # # negative control (fails)
    ["42.3 gcm-3", None],
    ["c40 °F", None],
    ["", None],
    ["*", None],
    ["*34gd", None],
    ['Index of refraction: 1.50920 @ 20 °C/D', None],
    ['Sound travels at 0.34 km/s', None],

]


@pytest.mark.parametrize("input_, output_", test_to_quantity)
def test_get_quantity(input_, output_):
    assert output_ == get_quantity(input_)


example_last_minute_sub = [
    [["5 degF"], ["5 degF"]]
]


@pytest.mark.parametrize("input_, output_", example_last_minute_sub)
def test_last_minute_sub(input_, output_):
    assert output_ == last_minute_sub(input_)
