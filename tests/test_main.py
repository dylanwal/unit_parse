import pytest

from unit_parse import Quantity, parser

examples = [
    # standard examples
    ["5", Quantity("5")],
    ["5 g", Quantity("5 g")],
    ["5 g/ml", Quantity("5 g/ml")],
    ["1 K", Quantity("1 kelvin")],
    ['40 °F', Quantity("40 degF")],
    ['-40 °F', Quantity('-40 degF')],
    ["170°C", Quantity('170 degC')],
    ['40°F', Quantity('40 degF')],
    ['20.80 mmHg', Quantity('20.80 mmHg')],
    ['20.80 mm Hg', Quantity('20.80 mmHg')],  # correcting a unit that pint gets wrong

    # scientific notation
    ["15*10**2 s", Quantity("15*10**2 s")],  # standard
    ["15*10^2 s", Quantity("15*10**2 s")],  # carrot symbol
    ["15 10**2 s", Quantity("15*10**2 s")],  # space for multiplication
    ["8.20x10**+1 ppm", Quantity("8.20*10**1 ppm")],  # x for multiplication
    ["8.20x10+1 ppm", Quantity("8.20*10**1 ppm")],  # no power symbol
    ['5e1 g/mol', Quantity('50 g/mol')],
    ['5E1 g/mol', Quantity('50 g/mol')],
    ['5 e1 g/mol', Quantity('50 g/mol')],
    ['5 E1 g/mol', Quantity('50 g/mol')],
    ['5e+1 g/mol', Quantity('50 g/mol')],
    ['5E-1 g/mol', Quantity('0.5 g/mol')],
    ['−66.11·10-62 ml/mol', Quantity('-66.11*10**-62 ml/mol')],
    ['−66.11·10+62 ml/mol', Quantity('-66.11*10**62 ml/mol')],
    ['−66.11·1062 ml/mol', Quantity('-66.11*10**62 ml/mol')],

    # messed up units/ units with powers
    ["2.3 gcm", Quantity("2.3 g*cm")],
    ["5e5 gmol/s", Quantity("5*10**5 g*mol/s")],
    ["2.3 gcm**3", Quantity("2.3 g*cm**3")],
    ["2.3 gcm**3", Quantity("2.3 g*cm^3")],
    ["2.3     g", Quantity("2.3 g")],
    ['1.10*10**-05 atm-m**3/mole', Quantity('1.10*10**-5 atm*m**3/mole')],
    ["-54.6e-5 atm-m**3/mole", Quantity("-54.6*10**-5 atm*m**3/mole")],
    ["2.3 mlgcm", Quantity("2.3 ml*g*cm")],
    ['42.3 gcm-3', Quantity('42.3 g*cm**-3')],
    ['42.3 g cm-3', Quantity('42.3 g*cm**-3')],
    ['−66.11·10-62 cm3/mol', Quantity('-66.11*10**-62 cm**3/mol')],
    ['−66.11·10+62 cm3/mol', Quantity('-66.11*10**62 cm**3/mol')],
    ['−66.11·1062 cm3/mol', Quantity('-66.11*10**62 cm**3/mol')],
    ["345.234 KCAL/MOLE", Quantity("345.234 kcal/mole")],

    # parenthesis (brackets turn into parenthesis)
    ["(4.0 °C)", Quantity("4 degC")],
    ["[4.0 °C]", Quantity("4 degC")],
    ["4.0 (°C)", Quantity("4 degC")],
    ["4.0 (°C))", Quantity("4 degC")],
    [")4.0 (°C)", Quantity("4 degC")],
    ["(4.0 (°C)", Quantity("4 degC")],
    ["()4.0 (°C)", Quantity("4 degC")],
    ['4.0 °C [39.2 g/[mol * s]]', [[Quantity("4 degC"), Quantity("39.2 g/(mol * s)")]]],
    ["1.0722 at 68 °F (EPA, 1998)", [[1.0722, Quantity("68 degF")]]],

    # conditions
    ["37.34 kJ/mole (at 25 °C)", [[Quantity("37.34 kJ/mole"), Quantity("25 degC")]]],
    ['20.8 mm Hg @ 25 °C', [[Quantity('20.8 mmHg'), Quantity('25 degC')]]],
    ['20.8 mm Hg (25 °C)', [[Quantity('20.8 mmHg'), Quantity('25 degC')]]],
    ['20.8 mm Hg at 25 °C', [[Quantity('20.8 mmHg'), Quantity('25 degC')]]],
    ["-4,395.63 kJ/mol at 25 °C", [[Quantity('-4395.63 kJ/mol'), Quantity('25 degC')]]],
    ["1.0A @ 25kW", [[Quantity('1.0A'), Quantity('25kW')]]],

    # list of quantities
    ['18 mm Hg; 20 mm Hg', Quantity('20 mmHg')],
    ['18 mm Hg @ 68 °F; 20 mm Hg @ 77° F',
     [[Quantity('18 mmHg'), Quantity('68 degF')], [Quantity('20 mmHg'), Quantity('77 degF')]]],
    ['18 mm Hg @ 68 °F ; 20 mm Hg @ 77° F (NTP, 1992)',
     [[Quantity('18 mmHg'), Quantity('68 degF')], [Quantity('20 mmHg'), Quantity('77 degF')]]],
    ['18 mm Hg at 68 °F ; 20 mm Hg at 77 °F',
     [[Quantity('18 mmHg'), Quantity('68 degF')], [Quantity('20 mmHg'), Quantity('77 degF')]]],
    ["Low threshold= 13.1150 mg/cu m; High threshold= 26840 mg/cu m; Irritating concn= 22875 mg/cu m.",
     Quantity('22875 mg/m**3')],
    ['Melting point: 75% -17.5 °C; 80% 4.6 °C; 85% 21 °C.', Quantity("4.6 degC")],

    # ranges
    ['115.2-115.3 °C', Quantity('115.2 degC')],
    ['115.2 - 115.3 °C', Quantity('115.2 degC')],
    ["1-2 °C",  Quantity('1 degC')],
    ["0-1 °C",  Quantity('0 degC')],
    ["10-20 ºC", Quantity('1e-20 degC')],
    ["11-20 ºC", Quantity('11 degC')],
    ["15 ± 5 ºC", Quantity('15 degC')],
    ["Between 10 and 20 ºC", Quantity('10 degC')],

    # words
    ["8.20x10+1 ppm; pure", Quantity("8.20*10**1 ppm")],
    ['40 °F (NTP, 1992)', Quantity("40 degF")],
    ['4.0 °C (39.2 °F) - closed cup', Quantity("4 degC")],
    ['4.0 °C [39.2 g/[mol * s]] - closed cup', [[Quantity("4 degC"), Quantity("39.2 g/(mol * s)")]]],
    ['4.0 °C [39.2 g/[mol * s] approx.] - closed cup', [[Quantity("4 degC"), Quantity("39.2 g/(mol * s)")]]],
    ['4.0 °C [39.2g/[mol*s] approx.] - closed cup', [[Quantity("4 degC"), Quantity("39.2 g/(mol * s)")]]],
    ['4.0 °C [39.2g/[mol*s]approx.] - closed cup', [[Quantity("4 degC"), Quantity("39.2 g/(mol * s)")]]],
    ['Detection in water: 0.73 ppm; Chemically pure', Quantity("0.73 ppm")],
    ['Odor Threshold Range: 0.15 to 25 ppm', Quantity("0.15 ppm")],
    ["0.05 ppm purity specified", Quantity("0.05 ppm")],
    ["Odor detection in air, 0.05 ppm (purity not specified)", Quantity("0.05 ppm")],
    ["Relative density (water = 1): 1.04-1.13", Quantity("1.04")],
    ["Density approximately 6.5 lb / gal.", Quantity("6.5 lb/ gal")],

    # duplicates of same quantity different units
    ["4.0 °C (39.2 °F)", Quantity("4 degC")],

    # complex
    ['18 mm Hg at 68 °F ; 20 mm Hg at 77° F (NTP, 1992)', [[Quantity('18 mmHg'), Quantity('68 degF')],
                                                           [Quantity('20 mmHg'), Quantity('77 degF')]]],
    ['Sound travels at 0.34 km/s', Quantity('0.34 km/s')],
    ['Pass me a 300 ml beer.', Quantity("300 ml")],
    ['13.565 kcal/mol at 25 °C; 10.60 kcal/mol at boiling point',
     [[Quantity("13.565 kcal/mol"), Quantity("25 °C")]]],

]


@pytest.mark.parametrize("input_, output_", examples)
def test_result_multi(input_, output_):
    assert output_ == parser(input_)


def test_main_error():
    with pytest.raises(TypeError):
        parser(1)
