import pint
u = pint.UnitRegistry()
U = Unit = u.Unit
Q = Quantity = u.Quantity

import unit_parse

a = 5 * U("in")
b = unit_parse.parser("5 cm")
c = a + b
print(c)
print("hi")
