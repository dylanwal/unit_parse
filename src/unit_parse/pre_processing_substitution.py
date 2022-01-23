from typing import List, Optional
import re

from . import config
from .logger import log_debug, log_info


@log_info
def remove_strings(text_in: str, remove_string: List[str]) -> str:
    """ Remove strings

    Go through text and delete all text that matches a remove_string

    Parameters
    ----------
    text_in: str
        Text to modify
    remove_string: List[str]
        Text you want to remove from string

    Returns
    -------
    text: str

    """
    for text in remove_string:
        text_in = text_in.replace(text, "")

    return text_in.strip()


@log_info
def substitution(text_in: str) -> str:
    """ substitution

    Preforms the standard series of substitutions.
    Which includes:
    * general substitutions
    * power (**, ^)
    * scientific notation
    * ranges

    Parameters
    ----------
    text_in: str

    Returns
    -------
    test: str

    """
    text_in = sub_general(text_in, patterns=config["pre_proc_sub"])
    text_in = sub_power(text_in)
    text_in = sub_sci_notation(text_in)
    text_in = reduce_ranges(text_in)

    return text_in.strip()


@log_debug
def sub_general(text_in: str, patterns: Optional[List[List[str]]]) -> str:
    """ substitutions general

    Performs general substitutions from regex expression.

    Parameters
    ----------
    text_in: str
        text to modify
    patterns: list[list[str]]
        Pattern and replacement values
        example:
        [
            # [search pattern, substitution value]
            ["^[a-zA-Z;,.: /]*", ""],  # remove text at front of strings
            ["(?<=[^a-zA-Z])at([^a-zA-Z])", " @ "],  # replace at with @
        ]

    Returns
    -------
    text: str

    """
    if isinstance(patterns, list):
        if isinstance(patterns[0], list):
            for pattern in patterns:
                text_in = re.sub(pattern[0], pattern[1], text_in)

            return text_in.strip()

    raise TypeError(f"Patterns must be a List[List[pattern, substitution]].")


@log_debug
def sub_power(text_in: str) -> str:
    """ substitution of powers

    Replaces:
    cm-3 with cm**-3.

    Parameters
    ----------
    text_in: str

    Returns
    -------
    text: str

    """
    found_unit_power = re.findall("[a-zA-Z]{1,10}[-+]?[0-4]", text_in)
    for exp in found_unit_power:
        if "-" in exp:
            exp_new = exp.replace("-", "**-", 1)
        elif "+" in exp:
            exp_new = exp.replace("+", "**", 1)
        else:
            exp_new = exp[:-1] + "**" + exp[-1]
        text_in = text_in.replace(exp, exp_new)

    return text_in.strip()


@log_debug
def sub_sci_notation(text_in: str) -> str:
    """ substitution of scientific notation

    Replaces:
    '10-62' with '10**-62'
    '10e-62' with '10**-62'
    '10E-62' with '10**-62'

    Parameters
    ----------
    text_in: str

    Returns
    -------
    text: str

    """
    found_sci_notation = re.findall("10[-+][0-9]{1,5}", text_in)  # '10-5' -> '10**-5'
    for exp in found_sci_notation:
        if "-" in exp:
            exp_new = exp.replace("-", "**-", 1)
        else:
            exp_new = exp.replace("+", "**", 1)
        text_in = text_in.replace(exp, exp_new)

    found_sci_notation = re.findall("[0-9]e[-+]?[0-9]{1,5}", text_in)
    for exp in found_sci_notation:
        exp_new = exp.replace("e", "*10**", 1)
        text_in = text_in.replace(exp, exp_new)

    found_sci_notation = re.findall("[0-9]E[-+]?[0-9]{1,5}", text_in)
    for exp in found_sci_notation:
        exp_new = exp.replace("E", "*10**", 1)
        text_in = text_in.replace(exp, exp_new)

    found_sci_notation = re.findall("[0-9][*]10[0-9]{1,5}", text_in)
    for exp in found_sci_notation:
        exp_new = exp.replace("10", "10**", 1)
        text_in = text_in.replace(exp, exp_new)

    found_sci_notation = re.findall("[0-9][ ]10[0-9]{1,5}", text_in)
    for exp in found_sci_notation:
        exp_new = exp.replace("10", "*10**", 1)
        text_in = text_in.replace(exp, exp_new)

    found_sci_notation = re.findall("[0-9][ ]{1,2}10[*]{2}[-+]?[0-9]{1,5}", text_in)
    for exp in found_sci_notation:
        exp_new = exp.replace(" 10**", "*10**", 1)
        text_in = text_in.replace(exp, exp_new)

    found_sci_notation = re.findall("[0-9][ ]{0,2}[e][*]{2}[-+]?[0-9]{1,5}", text_in)
    for exp in found_sci_notation:
        exp_new = exp.replace("e**", "*10**", 1)
        text_in = text_in.replace(exp, exp_new)

    found_sci_notation = re.findall("[0-9][ ]{0,2}[E][*]{2}[-+]?[0-9]{1,5}", text_in)
    for exp in found_sci_notation:
        exp_new = exp.replace("E**", "*10**", 1)
        text_in = text_in.replace(exp, exp_new)

    return text_in.strip()


@log_debug
def reduce_ranges(text_in: str) -> str:
    """ reduce ranges

    Replaces:
    '115.2-115.3 °C' with '115.2 °C'
    '115.2 - 115.3 °C' with '115.2 °C'

    Parameters
    ----------
    text_in: str

    Returns
    -------
    text: str

    Warning
    -------
    * Apply sub_sci_notation() first.

    """
    if bool(data_found := re.findall("[-.0-9]{1,6}[- ]{1,3}[-.0-9]{1,6}", text_in)):  # match ### - ### or ###-###
        reduced_range = re.findall("[-]?[.0-9]{1,6}[^0-9-,/; ]{0,8}", data_found[0])[0]
        return text_in.replace(data_found[0], reduced_range)
    else:
        return text_in.strip()
