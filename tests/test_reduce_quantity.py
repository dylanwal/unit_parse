import pytest

from unit_parse import Q, U, reduce_quantities
from unit_parse.utils import quantity_approx_equal

examples = [  # [Input, Output]
    # positive control (works, does changes)
    [[[[0.633, Q('68 degF')]], [[0.6709, Q('0.0')]], [[Q('40.89 pound / foot ** 3'), Q('35 degC')]],
      [[Q('0.2991 pound / foot ** 3'), Q('70 degC')]], Q('0.6'), 0.667, [[0.633, Q('68 degF')]], 2.09],
     [[Q('40.89 pound / foot ** 3'), Q('35 degC')]]],

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

    [[[[Q("68 degF"), Q("760.0 mmHg")]], Q("68.0 degF"), Q("20.0 degC"), Q("293.15 kelvin * speed_of_light ** 2"),
      Q("68 degF"), Q("68 degF")],
     [[Q("68 degF"), Q("760.0 mmHg")]]],

    [[[Q("68 degF"), Q("760.0 mmHg")], Q("68.0 degF"), Q("20.0 degC"), Q("293.15 kelvin * speed_of_light ** 2"),
      Q("68 degF"), Q("68 degF")],
     [[Q("68 degF"), Q("760.0 mmHg")]]],

    [[0.65, Q('0.66'), Q('0.65'), Q('0.65')], Q('0.65')],

    [[[0.65, Q('25  degC')], Q('0.65'), Q('0.65')], [[0.65, Q('25  degC')]]],

    [[[Q('50  kg'), Q('25  kg')], Q('0.65 dimensionless'), Q('0.65 dimensionless')],
     Q('50  kg')],

    [[6, 5, 5, 3, 4, 5], 5],
    [[6, 5, 3, 4, 7], 5],
    [[[6, 5, 5, 3, 4, 5], 5, 6], 5],
    [[Q("1 g"), Q("2 g"), Q("3 g"), Q("4 g"), Q("5 g")], Q("3 g")],
    [[Q("1 g"), Q("2 g"), Q("3 g"), Q("4 g"), Q("5 g"), Q("6 g")], Q("4 g")],
    [[[Q("6 g"), Q("6 g"), Q("5 g"), Q("5.5 g"), Q("6.2 g")], Q("6")],
     Q("6 g")],

    [[[[Q("-15 degC"), Q("1 mmHg")]], Q("-41.6 degC"), Q("-42 degC"), Q("-40 degC"), Q("-40 degC")],
     [[Q("-15 degC"), Q("1 mmHg")]]],

    [[[[Q("-1500 degC"), Q("1 mmHg")]], Q("-41.6 degC"), Q("-42 degC"), Q("-40 degC"), Q("-40 degC")],
     Q("-40 degC")],

    [[[Q("5 degC")], [[Q("5 degC")]], [[Q("5 degC")], Q("3 degC")], Q("5.4 degC"), 5.4], Q("5 degC")],

    [[[[Q('18 mmHg'), Q('68 degF')], [Q('20 mm_Hg'), Q('77 degF')]], Q('20.8 mmHg'), Q('2.0'), Q('16 mmHg'),
      Q('16 mmHg'), [[Q('16 mmHg'), Q('68 degF')], [Q('19 mm_Hg'), Q('77 degF')]]],
     [[Q('16 mmHg'), Q('68 degF')], [Q('19 mm_Hg'), Q('77 degF')]]],

    [[[Q("-41.6 degC"), Q("-50 degC"), Q("-60 degC")], Q("-40 degC"), Q("-41 degC"), Q("-42 degC")],
     Q("-41.6 degC")],

    [[Q("0 psi"), Q("0 psi"), Q("0 psi"), Q("0.1 psi")], Q("0 psi")],

    [[Q('25  degC')], Q('25  degC')],
    [[[Q('25  degC')]], Q('25  degC')],
    # negative control (fails/ does no changes)
    [Q('25  degC'), Q('25  degC')],

]


@pytest.mark.parametrize("input_, output_", examples)
def test_reduce_quantities(input_, output_):
    if isinstance(output_, Q):
        assert quantity_approx_equal(output_, reduce_quantities(input_))
    else:
        assert output_ == reduce_quantities(input_)


def test_prefer_unit():
    input_ = [Q("2 ppm"), Q("5 mol/ml"), Q("10 mol/cm**3")]
    output_ = Q("2 ppm")
    assert output_ == reduce_quantities(input_, prefer_unit=U("ppm"))


def test_order_error():
    with pytest.raises(ValueError):
        input_ = [Q("2 ppm"), Q("5 mol/ml"), Q("10 mol/cm**3")]
        reduce_quantities(input_, order=(1, 2, 3, 0, 4))
