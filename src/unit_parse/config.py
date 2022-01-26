import os
import sys

from unit_parse.logger import logger


def _get_from_stack(obj):
    """
    Gets object from Python stack/globals
    Stops at first object it finds

    """
    for i in range(100):  # 100 is to limit the depth it looks
        frames = sys._getframe(i)
        globals_ = frames.f_globals
        found_obj = [globals_[k] for k, v in globals_.items() if isinstance(v, obj) and k[0] != "_"]
        if found_obj:
            found_obj = found_obj[0]
            break
    else:
        mes = f"{obj} not found in globals."
        raise Exception(mes)

    return found_obj


def check_for_pint():
    """ Check for Pint

    Pint's requires a Unit Registry to be defined. However, Unit Registries are not interoperable and will throw
    errors if a unit from one registry is used in another. So we go looking to see if one has been created,
    and if it hasn't we will make one!

    Returns
    -------
    UnitRegistry

    """
    modules = sys.modules
    if "pint" in modules:
        logger.warning("'Pint' module found in stack. (you have 'import pint' somewhere in your code).")
        # get unit registry
        try:
            u = _get_from_stack(modules["pint.registry"].UnitRegistry)
            logger.warning("\033[32m Unit registry found. :) \033[0m")
            return u
        except Exception:
            logger.warning("Pint unit registry not found in stack. Loading 'unit_parser' registry. (Note: "
                           "Pint unit registries are not interoperable. ")

    # if no pint found, load local
    import pint
    current_path = os.path.dirname(os.path.realpath(__file__))
    return pint.UnitRegistry(autoconvert_offset_to_baseunit=True,
                             filename=os.path.join(current_path, "support_files\\default_en.txt"))


# set pint units
u = check_for_pint()
U = Unit = u.Unit
Q = Quantity = u.Quantity

# load english dictionary
file_path = os.path.dirname(os.path.realpath(__file__))
path_to_dict = os.path.join(file_path, "support_files\\dictionary.txt")
with open(path_to_dict, 'r') as file:
    english_dict = set(file.read().split("\n"))


class Config:
    """


    Attributes
    ----------
    pre_proc_sub : list[str]
        Pre-processing patterns
    pre_proc_split

    last_minute_sub

    english_dict: set
        A reduced set of english words that are removed from the parsing text.

    """

    def __init__(self):
        self.remove_text = []

        self.pre_proc_sub = [
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

        self.pre_proc_split = [";"]

        self.last_minute_sub = [
            # [pattern, substitution value]
            ["-{1}[^0-9]*$", ""],  # remove trailing dash
            ["(?<=[a-zA-Z0-9]) {1,2}[0-9()]{2,5}", ""]  # remove trailing number  ex. 90 g/mol 1999 ->  90 g/mol
        ]

        self.english_dict = english_dict


config = Config()
