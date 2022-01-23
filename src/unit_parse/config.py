import os

import pint

current_path = os.path.dirname(os.path.realpath(__file__))

u = pint.UnitRegistry(autoconvert_offset_to_baseunit=True, filename=os.path.join(current_path,
                                                                                 "support_files\\default_en.txt"))
U = Unit = u.Unit
Q = Quantity = u.Quantity

config = {
    "pre_proc_sub": [
        # [pattern, substitution value]
        ["^[a-zA-Z;,.: /]*", ""],  # remove text at front of strings
        ["(?<=[^a-zA-Z])at([^a-zA-Z])", " @ "],  # replace at with @
        ["−", "-"],  # unify dash (long, short) symbols
        ["·", "*"],  # unify multiplication symbols
        ["mm Hg", "mmHg"],  # pint gets confused
        ["° F", " °F"],  # pint gets confused (degree farad)
        ["° C", " °C"],  # pint gets confused
        ["(?<=[0-9]{1})[ ]{0,1}X[ ]{0,1}(?=[0-9]{1})", "*"],  # unify multiplication symbols
        ["(?<=[0-9]{1})[ ]{0,1}x[ ]{0,1}(?=[0-9]{1})", "*"],  # unify multiplication symbols
        ["\[", "("],  # make all brackets parenthesis
        ["\]", ")"],  # make all brackets parenthesis
        ["={1}.*$", ""],  # if equals in string take first term
        ["^.*:{1}", ""]  # delete everything in front of collen
    ],
    "pre_proc_split": [";"],
    "last_minute_sub": [
        # [pattern, substitution value]
        ["LB", "lb"],
        ["mm Hg", "mmHg"],
        ["kpa", "kPa"],
        ["-{1}[^0-9]*$", ""],
        ["° F", "°F"],
        ["° C", "°C"],
    ],

}
