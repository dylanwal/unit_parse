from typing import List
import re

from unit_parse.config import config
from unit_parse.logger import log_debug, log_info
from unit_parse.utils import contains_number, remove_empty_str


@log_info
def multiple_quantities_main(text_in: str) -> list[list[str]]:
    """

    Parameters
    ----------
    text_in

    Returns
    -------

    """
    text_list = multiple_quantities(text_in, sep=config.pre_proc_split)
    out = []
    for text in text_list:
        out.append(condition_finder(text))

    return out


@log_debug
def multiple_quantities(text_in: str, sep: list[str]) -> List[str]:
    """ multiple quantities

    Splits text into multiple quantities

    Parameters
    ----------
    text_in: str

    sep: list[str]
        separator between quantities

    Returns
    -------
    text: list[str]

    Examples
    --------


    """
    sep = "|".join(sep)
    result = re.split(sep, text_in)
    return [text.strip() for text in result]

def split_on_quantities(text_in: str) -> list[str]:
    """
    Split the string into a list of strings, where each string contains a single quantity.

    Examples
    --------
    '18 mm Hg @ 68 °F' --> ['18 mm Hg @', '68 °F']
    'Melting point: 75% -17.5 °C' --> ['Melting point: 75%', '-17.5 °C']
    'Pass me a 300 ml beer.' --> ['Pass me a 300 ml beer.']
    """
    # Use regular expression to split the input text into possible groups of quantities
    # The pattern looks for spaces (\s) followed by a digit [-]?(\d)
    # The positive lookahead (?=...) ensures that the split happens without
    # consuming the digit
    quantities = re.split(r'(\s+)(?=[-]?\d)', text_in)

    # This regex will sometimes produce groups of just text, so merge subsequent groups until
    # each group contains a number. This could be done in a more complex regex,
    # but a loop is pretty simple.
    results = []
    for result in quantities:
        if results and not contains_number(results[-1]):
            results[-1] = results[-1] + result
        else:
            results.append(result)
    return results


@log_debug
def condition_finder(text_in: str) -> List[str]:
    """
    Extracts conditions and creates list [quantity, conditions]

    Parameters
    ----------
    text_in: str

    Returns
    -------
    list_text: list[str], str

    Examples
    --------
    '18 mm Hg @ 68 °F ' --> ['18 mm Hg', '68 °F']
    ' 20 mm Hg @ 77° F (NTP, 1992)' --> ['20 mm Hg', '77° F', 'NTP, 1992']

    Warnings
    --------
    * replace 'at' with '@' first (use sub_general in pre_processing.py)

    """
    out = []

    if "(" in text_in or ")" in text_in:
        out += reduce_parenthesis(text_in)
    else:
        out.append(text_in)

    out2 = []
    for text in out:
        if "@" in text:
            result = re.split("@", text)
            out2 += [t.strip() for t in result]
        else:
            result = split_on_quantities(text)
            out2 += result

    return [text.strip() for text in out2]


@log_debug
def reduce_parenthesis(text_in: str) -> List[str]:
    """ reduce parenthesis

    Called recursively.
    Removes one layer of parenthesis and breaks the string into parts.

    Parameters
    ----------
    text_in: str

    Returns
    -------
    list_text: list[str]

    Examples
    --------
    "(aaaaa)" --> "aaaaa"
    "(aa(a)aa)" --> "aa(a)aa"
    "(aaa)(aa)" --> ["aaa", "aa"]

    """
    # guard statement
    if "(" not in text_in and ")" not in text_in:
        return [text_in]

    text_in = text_in.strip()

    # get inner parenthesis slice
    open_index = get_char_index(text_in, "(")
    close_index = get_char_index(text_in, ")")

    # remove single unbalanced parenthesis and return
    if len(open_index) == 0:
        return remove_empty_str(text_in.split(")"))
    elif len(close_index) == 0:
        return remove_empty_str(text_in.split("("))

    # find first-inner () pair
    for largest_open_index in reversed(open_index):
        if largest_open_index > close_index[0]:
            continue
        else:
            slice_ = slice(largest_open_index+1, close_index[0])
            text_list = [
                text_in[:(slice_.start-1)],
                text_in[slice_],
                text_in[(slice_.stop+1):]
            ]
            # Check for division sign and don't brake those up (use brackets as temp place holder)
            if text_list[0].strip().endswith("/"):
                text_list = [text_list[0] + "[" + text_list[1] + "]", text_list[-1]]

            text_list = remove_empty_str(text_list)
            break
    else:  # situation ')text('
        return remove_empty_str(re.split("[()]", text_in))

    # call recursively
    if len(open_index) > 1 or len(close_index) > 1:
        text_list_out = []
        for text in text_list:
            text_list_out += reduce_parenthesis(text)

        text_list = remove_empty_str(text_list_out)

    return [text.replace("[", "(").replace("]", ")") for text in text_list]


def get_char_index(text_in: str, symbol: str) -> list[int]:
    """

    Looks for the first complete parenthesis pair.

    Parameters
    ----------
    text_in
    symbol

    Returns
    -------
    indexes: list[int]

    """
    return [pos for pos, char in enumerate(text_in) if char == symbol]
