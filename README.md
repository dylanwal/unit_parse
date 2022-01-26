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

Pass string you want to parse to `parser()`.

```python
from unit_parse import parser

result = parser("1.23 g/cm3 (at 25 °C)")
print(result) # [[<Quantity(1.23, 'gram / centimeter ** 3')>, <Quantity(25, 'degree_Celsius')>]]
```
'Quantity' are [pint quantities](https://pint.readthedocs.io/en/stable/defining-quantities.html). 

### Output structure
* **Parse unsuccessful**: None
* **Single value:** quantity
    * `5 g/mol`
* **Single value with condition:** [[quantity, condition]]  
    * `[['25 degC', '1 bar']]`
    * boil temperature is 25 °C at 1 bar of pressure
* **Multiple values:**  [quantity, quantity, ...] 
    * `[25 degC, 50 degC]`
* **Multiple values with conditions:** [[quantity, condition], [quantity, condition], ...]
    * `[['25 degC', '1 bar'], ['50 degC', '5 bar'], ['100 degC', '10 bar']]`

### Merging Quantities

Some times when you are doing parsing, you get multiple values from the parser. So it would be nice to reduce it 
down just to one value/value+condition/series+condition. `reduce_quantities` does exactly that!

It will group approximate equivalent quantities and throw out bad units (units that are not like the most common). 
You can select your preference for return priority with the `order` parameter. 

```python
from unit_parse import Quantity, reduce_quantities
  
quantities = [Quantity("68 degree_Fahrenheit"), Quantity("68.0 degree_Fahrenheit"), Quantity("20.0 degree_Celsius"),
              Quantity("293.15 kelvin * speed_of_light ** 2")]
  
result = reduce_quantities(quantities)
print(result)  # Quantity("68 degF")],
```


---
## Logging

The logger can be used to track the parsing steps.

Default level is warning.

warning: will only let you know if there is any text that is being ignored in the parsing process.
info: will show the major parsing steps.
debug: will show fine grain parsing steps.

### Example: INFO

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

### Example: DEBUG
Code:

```python
import logging

from unit_parse import parser, logger

logger.setLevel(logging.DEBUG)

result = parser("37.34 kJ/mole (at 25 °C)")
print(result) 
```

Output:

```console
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


---
## Configuration

The parser has a few configurations exposed to make it easy to modify how the works.

### Remove words

Text you want removed prior to parsing. 

Default is None. (Note: the parser naturally takes care of alot of 'bad' text)

```python
import unit_parse

remove_words = ["approx.", "roughly", "close to"]
unit_parse.config.remove_text = remove_words

result = unit_parse.parser("approx. 100 grams")
print(result)  # Quantity("100 gram")
```

### Pre-Processing Substitutions

Text you want to replace with another. 

Default there is a big list. Regex or text is accepted.

**Defaults:**
```python
pre_proc_sub = [
  # [pattern, substitution value]
  ["^[a-zA-Z;,.: /]*", ""],  # remove text at front of strings
  ["(?<=[^a-zA-Z])at([^a-zA-Z])", " @ "],  # replace at with @
  ["−", "-"],  # unify dash (long, short) symbols
  ["·", "*"],  # unify multiplication symbols
  ["° F", " °F"],  # pint gets confused (degree farad)
  ["° C", " °C"],  # pint gets confused
  ["°F", "degF"],  # eliminates issue with capitalization step
  ["°C", "degC"],  # eliminates issue with capitalization step
  ["(?<=[0-9]{1})[ ]{0,1}X[ ]{0,1}(?=[0-9]{1})", "*"],  # unify multiplication symbols
  ["(?<=[0-9]{1})[ ]{0,1}x[ ]{0,1}(?=[0-9]{1})", "*"],  # unify multiplication symbols
  ["\[", "("],  # make all brackets parenthesis
  ["\]", ")"],  # make all brackets parenthesis
  ["^.*={1}", ""],  # delete everything in front of equal
  ["^.*:{1}", ""],  # delete everything in front of collen
  ["( to )", "-"],   # unify how range are represented
  ["(?<=[a-zA-Z])-(?=[a-zA-Z])", " "],  # turn dashes between text into spaces so dictionary can remove
  ["mm Hg", "mmHg"],  # pint gets confused
  ["KG", "kg"],  # pint gets confused
  ["LB", "lb"],  # pint gets confused
  ["kpa", "kPa"],  # pint gets confused
  ["cu ft", "ft**3"],  # pint gets confused
  ["cu in", "in**3"],  # pint gets confused
  ["cu m", "m**3"],  # pint gets confused
  ["cu cm", "cm**3"],  # pint gets confused
  ["cu mm", "mm**3"],  # pint gets confused
]
```


```python
import unit_parse

more_pre_processing = [["MOL", "mol"]] # [bad text/regex, new text]
unit_parse.config.pre_proc_sub += more_pre_processing  # Here we are adding to the existing list

result = unit_parse.parser("100 MOL")  # pint is case-sensitive, so this will result in an invalid unit
print(result)  # Quantity("100 mole")
```

### Last Minute Substitutions

Text you want to replace with another, but happens at the very last stage before trying to convert to a unit. You 
should try to use pre-substitutions first, but there can be some situations where you want to do substitutions at a 
semi-parsed quantity.  

Default there is a big list. Regex or text is accepted.

**Defaults:**
```python
last_minute_sub = [
  # [pattern, substitution value]
  ["-{1}[^0-9]*$", ""],  # remove trailing dash
  ["(?<=[a-zA-Z0-9]) {1,2}[0-9()]{2,5}", ""]  # remove trailing number  ex. 90 g/mol 1999 ->  90 g/mol
]
```


```python
import unit_parse
        
more_last_minute_sub = [["MOL", "mol"]] # [bad text/regex, new text]
unit_parse.config.last_minute_sub += more_last_minute_sub # Here we are adding to the existing list

result = unit_parse.parser("100 MOL")  # pint is case-sensitive, so this will result in an invalid unit
print(result)  # Quantity("100 mole")
```


---
## Notes

### Pint UnitRegistry
Pint's requires a Unit Registry to be defined. However, Unit Registries are not interoperable and will throw 
errors if a unit from one registry is used in another. Unit_Parse will go looking to see if one has been created, 
and if it hasn't we will make one!

So if your project uses Pint already, make sure you import Pint and define the UnitRegistry before importing unit_parse.
    