# Unit Parse (unit_parse)

---
---
![PyPI](https://img.shields.io/pypi/v/unit_parse)
![tests](https://raw.githubusercontent.com/dylanwal/unit_parse/master/tests/badges/tests-badge.svg)
![coverage](https://raw.githubusercontent.com/dylanwal/unit_parse/master/tests/badges/coverage-badge.svg)
![flake8](https://raw.githubusercontent.com/dylanwal/unit_parse/master/tests/badges/flake8-badge.svg)
![downloads](https://static.pepy.tech/badge/unit_parse)
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

[Pint](https://github.com/hgrecco/pint) - Provides unit conversions of cleaned and parsed quantities.

---
---

## Usage

### Basics

Pass string you want to parse to `parser()`.

```python
from unit_parse import parser

result = parser("1.23 g/cm3 (at 25 °C)")
print(result) # [[<Quantity(1.23, 'g / cm ** 3')>, <Quantity(25, 'degC')>]]
```
'Quantity' are [pint quantities](https://pint.readthedocs.io/en/stable/defining-quantities.html). 

### Output structure
* **Parse unsuccessful**: None
* **Single value:** quantity
    * `5 g/mol`
* **Single value with condition:** [[quantity, condition]]  
    * `[['25 degC', '1 bar']]`
    * boil temperature is 25 °C at 1 bar of pressure
* **Multiple values with conditions:** [[quantity, condition], [quantity, condition], ...]
    * `[['25 degC', '1 bar'], ['50 degC', '5 bar'], ['100 degC', '10 bar']]`

### Merging Quantities

Sometimes when you are doing parsing, you get multiple values from the parser. So it would be nice to reduce it 
down just to one value/value+condition/series+condition. `reduce_quantities` does exactly that!

It will group approximate equivalent quantities and throw out bad units (units that are not like the most common). 
You can select your preference for return priority with the `order` parameter. 

```python
from unit_parse import Quantity, reduce_quantities
  
quantities = [Quantity("68 degF"), Quantity("68.0 degF"), Quantity("20.0 degC"),
              Quantity("293.15 kelvin * speed_of_light ** 2")]
  
result = reduce_quantities(quantities)
print(result)  # Quantity("68 degF")
```

---
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
    5 --> 5
    5 g --> 5 g
    5 g/ml --> 5.0 g / ml
    1 K --> 1 K
    40 °F --> 40 °F
    -40 °F --> -40 °F
    170°C --> 170 °C
    40°F --> 40 °F
    20.80 mmHg --> 20.8 mmHg
    20.80 mm Hg --> 20.8 mmHg
# scientific notation
    15*10**2 s --> 1500 s
    15*10^2 s --> 1500 s
    15 10**2 s --> 1500 s
    8.20x10**+1 ppm --> 82.0 ppm
    8.20x10+1 ppm --> 82.0 ppm
    5e1 g/mol --> 50.0 g / mol
    5E1 g/mol --> 50.0 g / mol
    5 e1 g/mol --> 50.0 g / mol
    5 E1 g/mol --> 50.0 g / mol
    5e+1 g/mol --> 50.0 g / mol
    5E-1 g/mol --> 0.5 g / mol
    −66.11·10-62 ml/mol --> -6.611e-61 ml / mol
    −66.11·10+62 ml/mol --> -6.611e+63 ml / mol
    −66.11·1062 ml/mol --> -6.611e+63 ml / mol
# messed up units/ units with powers
    2.3 gcm --> 2.3 cm * g
    5e5 gmol/s --> 500000.0 g * mol / s
    2.3 gcm**3 --> 2.3 cm**3 * g
    2.3 gcm**3 --> 2.3 cm**3 * g
    2.3     g --> 2.3 g
    1.10*10**-05 atm-m**3/mole --> 1.1000000000000001e-05 atm * m**3 / mol
    -54.6e-5 atm-m**3/mole --> -0.000546 atm * m**3 / mol
    2.3 mlgcm --> 2.3 cm * g * ml
    42.3 gcm-3 --> 42.3 g / cm**3
    42.3 g cm-3 --> 42.3 g / cm**3
    −66.11·10-62 cm3/mol --> -6.611e-61 cm**3 / mol
    −66.11·10+62 cm3/mol --> -6.611000000000001e+63 cm**3 / mol
    −66.11·1062 cm3/mol --> -6.611000000000001e+63 cm**3 / mol
    345.234 KCAL/MOLE --> 345.234 kcal / mol
# parenthesis (brackets turn into parenthesis)
    (4.0 °C) --> 4.0 °C
    [4.0 °C] --> 4.0 °C
    4.0 (°C) --> 4.0 °C
    4.0 (°C)) --> 4.0 °C
    )4.0 (°C) --> 4.0 °C
    (4.0 (°C) --> 4.0 °C
    ()4.0 (°C) --> 4.0 °C
    4.0 °C [39.2 g/[mol * s]] --> [[<Quantity(4.0, 'degree_Celsius')>, <Quantity(39.2, 'gram / mole / second')>]]
    1.0722 at 68 °F (EPA, 1998) --> [[1.0722, <Quantity(68, 'degree_Fahrenheit')>]]
# conditions
    37.34 kJ/mole (at 25 °C) --> [[<Quantity(37.34, 'kilojoule / mole')>, <Quantity(25, 'degree_Celsius')>]]
    20.8 mm Hg @ 25 °C --> [[<Quantity(20.8, 'millimeter_Hg')>, <Quantity(25, 'degree_Celsius')>]]
    20.8 mm Hg (25 °C) --> [[<Quantity(20.8, 'millimeter_Hg')>, <Quantity(25, 'degree_Celsius')>]]
    20.8 mm Hg at 25 °C --> [[<Quantity(20.8, 'millimeter_Hg')>, <Quantity(25, 'degree_Celsius')>]]
    -4,395.63 kJ/mol at 25 °C --> [[<Quantity(-4395.63, 'kilojoule / mole')>, <Quantity(25, 'degree_Celsius')>]]
# list of quantities
    18 mm Hg; 20 mm Hg --> 20 mmHg
    18 mm Hg @ 68 °F; 20 mm Hg @ 77° F --> [[<Quantity(18, 'millimeter_Hg')>, <Quantity(68, 'degree_Fahrenheit')>], [<Quantity(20, 'millimeter_Hg')>, <Quantity(77, 'degree_Fahrenheit')>]]
    18 mm Hg @ 68 °F ; 20 mm Hg @ 77° F (NTP, 1992) --> [[<Quantity(18, 'millimeter_Hg')>, <Quantity(68, 'degree_Fahrenheit')>], [<Quantity(20, 'millimeter_Hg')>, <Quantity(77, 'degree_Fahrenheit')>]]
    18 mm Hg at 68 °F ; 20 mm Hg at 77 °F --> [[<Quantity(18, 'millimeter_Hg')>, <Quantity(68, 'degree_Fahrenheit')>], [<Quantity(20, 'millimeter_Hg')>, <Quantity(77, 'degree_Fahrenheit')>]]
    Low threshold= 13.1150 mg/cu m; High threshold= 26840 mg/cu m; Irritating concn= 22875 mg/cu m. --> 22875.0 mg / m**3
# ranges
    115.2-115.3 °C --> 115.2 °C
    115.2 - 115.3 °C --> 115.2 °C
# words
    8.20x10+1 ppm; pure --> 82.0 ppm
    40 °F (NTP, 1992) --> 40 °F
    4.0 °C (39.2 °F) - closed cup --> 4.0 °C
    4.0 °C [39.2 g/[mol * s]] - closed cup --> [[<Quantity(4.0, 'degree_Celsius')>, <Quantity(39.2, 'gram / mole / second')>]]
    4.0 °C [39.2 g/[mol * s] approx.] - closed cup --> [[<Quantity(4.0, 'degree_Celsius')>, <Quantity(39.2, 'gram / mole / second')>]]
    4.0 °C [39.2g/[mol*s] approx.] - closed cup --> [[<Quantity(4.0, 'degree_Celsius')>, <Quantity(39.2, 'gram / mole / second')>]]
    4.0 °C [39.2g/[mol*s]approx.] - closed cup --> [[<Quantity(4.0, 'degree_Celsius')>, <Quantity(39.2, 'gram / mole / second')>]]
    Detection in water: 0.73 ppm; Chemically pure --> 0.73 ppm
    Odor Threshold Range: 0.15 to 25 ppm --> 0.15 ppm
    0.05 ppm purity specified --> 0.05 ppm
    Odor detection in air, 0.05 ppm (purity not specified) --> 0.05 ppm
    Relative density (water = 1): 1.04-1.13 --> 1.04
    Density approximately 6.5 lb / gal. --> 6.5 lb / gal
# duplicates of same quantity different units
    4.0 °C (39.2 °F) --> 4.0 °C
    -7991 cal/g = -334.6X10+5 J/KG --> -33460000.000000004 J / kg
# complex
    18 mm Hg at 68 °F ; 20 mm Hg at 77° F (NTP, 1992) --> [[<Quantity(18, 'millimeter_Hg')>, <Quantity(68, 'degree_Fahrenheit')>], [<Quantity(20, 'millimeter_Hg')>, <Quantity(77, 'degree_Fahrenheit')>]]
    Sound travels at 0.34 km/s --> 0.34 km / s
    Pass me a 300 ml beer. --> 300 ml
```


Stuff it gets wrong. No one is perfect!
```python
Index of refraction: 1.50920 @ 20 °C/D --> [[1.5092, <Quantity(293.15, 'kelvin / debye')>]]
Vapor pressure, kPa at 20 °C: 2.0 --> 2.0
Specific optical rotation @ 15 °C/D + 230 deg (concn by volume = 1.8 in chloroform) --> 1.8
```

---
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
---

## Notes

### Pint UnitRegistry

Pint's requires a Unit Registry to be defined. However, Unit Registries are not interoperable and will throw
errors if a unit from one registry is used in another. Unit_Parse will go looking to see if one has been created,
and if it hasn't we will make one!

So if your project uses Pint already, make sure you import Pint and define the `UnitRegistry` before
importing `unit_parse`. You must also define `Unit` and `Quantity` to make the registry discoverable.

```python
import pint

u = pint.UnitRegistry()
U = Unit = u.Unit
Q = Quantity = u.Quantity

from unit_parse import parser

# your code from here…
```
    
