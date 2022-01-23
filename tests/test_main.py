import pytest

from unit_parse import Quantity


examples = [
    ["8.20x10+1 ppm; pure", Quantity("8.20*10**1 ppm")],
    ["37.34 kJ/mole (at 25 °C)", [Quantity("37.34 kJ/mole"), Quantity("25 degC")]],
    ['40 °F (NTP, 1992)', Quantity("40 degF")],
    ['4.0 °C (39.2 °F) - closed cup', [Quantity("4 degC")]],
    ['4.0 °C [39.2 g/[mol * s]] - closed cup', [Quantity("4 degC"), Quantity("39.2 g/(mol * s)")]],
    ['4.0 °C [39.2 g/[mol * s] approx.] - closed cup', [Quantity("4 degC"), Quantity("39.2 g/(mol * s)")]],
    ['4.0 °C [39.2g/[mol*s] approx.] - closed cup', [Quantity("4 degC"), Quantity("39.2 g/(mol * s)")]],
    ['4.0 °C [39.2g/[mol*s]approx.] - closed cup', [Quantity("4 degC"), Quantity("39.2 g/(mol * s)")]],
    ['42.3 gcm-3', Quantity('42.3 g*cm**-3')],
    ['42.3 g cm-3', Quantity('42.3 g*cm**-3')],
    ['40°F', Quantity('40 degF')],
    ['40 °F', Quantity('40 degF')],
    ['115.2-115.3 °C', Quantity('115.2 degC')],
    ['115.2 - 115.3 °C', Quantity('115.2 degC')],
    ['-40 °F', Quantity('-40 degF')],
    ['20.80 mmHg', Quantity('20.80 mmHg')],
    ['18 mm Hg at 68 °F ; 20 mm Hg at 77° F (NTP, 1992)', [[Quantity('18 mmHg'), Quantity('68 degF')],
                                                           [Quantity('20 mmHg'), Quantity('77 degF')]]],
    ['20.8 mm Hg @ 25 °C', [Quantity('20.8 mmHg'), Quantity('25 degC')]],
    ['20.8 mm Hg (25 °C)', [Quantity('20.8 mmHg'), Quantity('25 degC')]],
    ['20.8 mm Hg at 25 °C', [Quantity('20.8 mmHg'), Quantity('25 degC')]],
    ['5e1 g/mol', Quantity('50 g/mol')],
    ['−66.11·10-62 cm3/mol', Quantity('-66.11*10**-62 cm**3/mol')],
    ['−66.11·10+62 cm3/mol', Quantity('-66.11*10**62 cm**3/mol')],
    ['−66.11·1062 cm3/mol', Quantity('-66.11*10**62 cm**3/mol')],
    ['-14.390 BTU/LB= -7992 CAL/G= -334.6X10+5 J/KG', Quantity('-14.390 BTU/lb')],

    ['Sound travels at 0.34 km/s', Quantity('0.34 km/s')],
    ['Pass me a 300 ml beer.', Quantity("300 ml")],

    ['Index of refraction: 1.50920 @ 20 °C/D', [Quantity('1.50920'), Quantity('20 degC')]],
    ['Vapor pressure, kPa at 20 °C: 2.0', [Quantity('2.0 kPa'), Quantity('20 degC')]],
]


