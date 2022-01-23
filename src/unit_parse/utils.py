from typing import List, Any, Optional, Union
import re

from . import Quantity


def quantity_approx_equal(quantity1: Quantity, quantity2: Quantity, cutoff: Optional[float] = 0.02) -> bool:
    """ Returns T/F for any two quantities"""
    if not isinstance(quantity1, Quantity) or not isinstance(quantity2, Quantity):
        return False

    if quantity1.dimensionality == quantity2.dimensionality and \
            abs((quantity1 - quantity2) / quantity2) <= cutoff:
        return True

    return False


def flatten_list(list_in: List[Any]) -> List[Any]:
    """
    Turns nested lists into a single level list.
    List[List[List[...]]]  -> List[]
    """
    if not isinstance(list_in, list):
        return list_in

    list_out = []
    for _obj in list_in:
        if isinstance(_obj, list):
            list_out += flatten_list(_obj)
        else:
            list_out.append(_obj)

    return list_out


def remove_empty_str(list_in: List[Any]) -> List[Any]:
    """ Remove empty strings ('' or ' ' or '    ') from list."""
    out = []
    for obj in list_in:
        if isinstance(obj, str):
            obj.strip()
            if obj.strip() != "":
                out.append(obj)
        else:
            out.append(obj)

    return out
    # return list(filter(None, list_in))


def contains_number(obj_in: str) -> bool:
    """ Checks list to see if it has a number in it anywhere."""
    if isinstance(obj_in, str):
        return bool(re.search('\d', obj_in))
    else:
        raise TypeError


def sig_figs(number: Union[float, int], sig_digit: int = 3) -> Union[int, float]:
    """ significant figures

    Given a number return a string rounded to the desired significant digits.

    Parameters
    ----------
    number: float, int
        number you want to reduce significant figures on
    sig_digit: int
        significant digits

    Returns
    -------
    number: int, float

    """
    if isinstance(number, float):
        return float('{:.{p}g}'.format(number, p=sig_digit))
    elif isinstance(number, int):
        return float('{:.{p}g}'.format(number, p=sig_digit))
    else:
        raise TypeError(f"'sig_figs' only accepts int or float. Given: {number} (type: {type(number)}")


def split_list(text_split: List[Union[str, Any]], chunks: Union[str, List[str]], maxsplit: int = 1) \
        -> List[Union[str, Any]]:
    """Splits text up into a list of strings based on chunks."""
    if isinstance(chunks, str):
        chunks = [chunks]
    if isinstance(text_split, str):
        text_split = [text_split]
    if not isinstance(text_split, list):
        return text_split

    for chunk in chunks:
        for i, text in enumerate(text_split):
            if isinstance(text, str) and chunk in text:
                split_cell = text_split.pop(i).split(chunk, maxsplit=maxsplit)  # split cell into 2
                split_cell.insert(1, chunk)  # insert chunk back into middle
                split_cell = [cell for cell in split_cell if cell]  # remove empty strings ""
                for ii, cell in enumerate(split_cell):
                    # re-add the new split cells back into list in the correct position
                    text_split.insert(i+ii, cell)
                break

    return text_split


def get_list_depth(list_) -> int:
    """ Get the number of nesting of list """
    if isinstance(list_, list):
        return 1 + max(get_list_depth(item) for item in list_)
    else:
        return 0
