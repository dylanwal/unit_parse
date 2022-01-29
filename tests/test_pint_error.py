import pytest

import pint

from unit_parse import parser

u = pint.UnitRegistry()
U = Unit = u.Unit
Q = Quantity = u.Quantity


def test_import():
    assert 5 * U("cm") == parser("5 cm")
