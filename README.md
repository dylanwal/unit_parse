# Unit Parse (unit_parse)

---
---
![PyPI](https://img.shields.io/pypi/v/unit_parse)
![tests](https://raw.githubusercontent.com/dylanwal/unit_parse/master/tests/badges/tests-badge.svg)
![coverage](https://raw.githubusercontent.com/dylanwal/unit_parse/master/tests/badges/coverage-badge.svg)
![flake8](https://raw.githubusercontent.com/dylanwal/unit_parse/master/tests/badges/flake8-badge.svg)
![downloads](https://img.shields.io/pypi/dm/unit_parse)
![license](https://img.shields.io/github/license/dylanwal/unit_parse)

Do you have strings/text that you want to turn into quantities?

Are you trying to clean scientific data you extracted from [Wikipida](https://en.wikipedia.org/wiki/Main_Page) or some 
other sketchy website?

Try 'Unit_Parse' to clean everything up for you!

#### Description: 
'Unit_Parse' is built on top of [Pint](https://github.com/hgrecco/pint). It was specifically designed to handle data 
that was extracted from scientific work. It has been rigorously tested against chemistry data 
extracted from Wikipida (example: [styrene](https://en.wikipedia.org/wiki/Styrene); density, melting point, boiling 
point, etc.) and data from [PubChem](https://pubchem.ncbi.nlm.nih.gov/) 
(example: [styrene](https://pubchem.ncbi.nlm.nih.gov/compound/Styrene) ; density, melting point, flash point, etc.).

---

## Installation

```
pip install unit_parse
```

## Dependencies

[Pint]((https://github.com/hgrecco/pint)) - Provides unit conversions of cleaned and parsed quantities.

---
---

## Usage

### Basics

```python
from unit_parse import parser

result = parser("37.34 kJ/mole (at 25 °C)")
print(result)
```

---
## Logging

The logger can be used to track how a text that through the parsing steps.
Default level is warning.

warning: will only let you know if there is any text that is being ignored in the parsing process.
info: will show the major parsing steps.
debug: will show fine grain parsing steps.

### Example INFO

Code:

```python
import logging

from unit_parse import parser, logger

logger.setLevel(logging.INFO)

result = parser("37.34 kJ/mole (at 25 °C)")
print(result)
```

Output:

```console
    INPUT: 37.34 kJ/mole (at 25 °C)
    substitution: ('37.34 kJ/mole (at 25 °C)',) --> 37.34 kJ/mole ( @ 25 °C)
    multiple_quantities_main: ('37.34 kJ/mole ( @ 25 °C)',) --> [['37.34 kJ/mole', '', '25 °C']]
    text_list_to_quantity: ([['37.34 kJ/mole', '', '25 °C']],) --> [[<Quantity(37.34, 'kilojoule / mole')>, <Quantity(25, 'degree_Celsius')>]]
    remove_duplicates: ([[<Quantity(37.34, 'kilojoule / mole')>, <Quantity(25, 'degree_Celsius')>]],) --> [[<Quantity(37.34, 'kilojoule / mole')>, <Quantity(25, 'degree_Celsius')>]]
    OUTPUT: [<Quantity(37.34, 'kilojoule / mole')>, <Quantity(25, 'degree_Celsius')>]
[<Quantity(37.34, 'kilojoule / mole')>, <Quantity(25, 'degree_Celsius')>]
```

### Example DEBUG
Code:

```python
import logging

from unit_parse import parser, logger

logger.setLevel(logging.DEBUG)

result = parser("37.34 kJ/mole (at 25 °C)")
print(result)
```

Output:

```
    INPUT: 37.34 kJ/mole (at 25 °C)
        sub_general: ('37.34 kJ/mole (at 25 °C)',) --> 37.34 kJ/mole ( @ 25 °C)
        sub_power: ('37.34 kJ/mole ( @ 25 °C)',) --> 37.34 kJ/mole ( @ 25 °C)
        sub_sci_notation: ('37.34 kJ/mole ( @ 25 °C)',) --> 37.34 kJ/mole ( @ 25 °C)
        reduce_ranges: ('37.34 kJ/mole ( @ 25 °C)',) --> 37.34 kJ/mole ( @ 25 °C)
    substitution: ('37.34 kJ/mole (at 25 °C)',) --> 37.34 kJ/mole ( @ 25 °C)
        multiple_quantities: ('37.34 kJ/mole ( @ 25 °C)',) --> ['37.34 kJ/mole ( @ 25 °C)']
        reduce_parenthesis: ('37.34 kJ/mole ( @ 25 °C)',) --> ['37.34 kJ/mole ', ' @ 25 °C']
        condition_finder: ('37.34 kJ/mole ( @ 25 °C)',) --> ['37.34 kJ/mole', '', '25 °C']
    multiple_quantities_main: ('37.34 kJ/mole ( @ 25 °C)',) --> [['37.34 kJ/mole', '', '25 °C']]
        get_quantity_and_cond: (['37.34 kJ/mole', '', '25 °C'],) --> [<Quantity(37.34, 'kilojoule / mole')>, <Quantity(25, 'degree_Celsius')>]
    text_list_to_quantity: ([['37.34 kJ/mole', '', '25 °C']],) --> [[<Quantity(37.34, 'kilojoule / mole')>, <Quantity(25, 'degree_Celsius')>]]
    remove_duplicates: ([[<Quantity(37.34, 'kilojoule / mole')>, <Quantity(25, 'degree_Celsius')>]],) --> [[<Quantity(37.34, 'kilojoule / mole')>, <Quantity(25, 'degree_Celsius')>]]
    OUTPUT: [<Quantity(37.34, 'kilojoule / mole')>, <Quantity(25, 'degree_Celsius')>]
[<Quantity(37.34, 'kilojoule / mole')>, <Quantity(25, 'degree_Celsius')>]
```

---
---
## Examples

Yep, there's alot of them! 

```python
    # Simple conversions
    5 -> 5 dimensionless
    5 g -> 5 gram
    5 g/ml -> 5.0 gram / milliliter
    1 K -> 1 kelvin

    # stuff
```