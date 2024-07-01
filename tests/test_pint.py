import pint
u = pint.UnitRegistry()
U = Unit = u.Unit
Q = Quantity = u.Quantity

from unit_parse import parser


def test_import():
    assert 5 * U("cm") == parser("5 cm")
