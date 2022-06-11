import sexpdata
from sexpdata import loads


def load(raw_string: str):
    """
    Returns a list of S-Expression Symbols.
    """
    return loads(raw_string, true="yes", false="no", line_comment="#")


def get_symbol_value(item):
    """
    Returns the value of the topmost child of an S-Expression Symbol.
    Example:    item = (user (name John) (surname Doe))
                return 'user'
    """
    if type(item) != sexpdata.Symbol:
        name = get_symbol_value(sexpdata.car(item))
    else:
        name = item.value()
    return name


def get_symbol_data(item, index=0):
    """
    Returns the element at a given index inside an S-Expression Symbol.
    Example:    item = (user (name John) (surname Doe))
                return (name John)
    """
    cons = sexpdata.cdr(item)[index]
    if type(cons) == sexpdata.Symbol:
        data = cons.value()
    else:
        data = cons
    return data


def get_symbol_data_by_token(item, token, recursive=True):
    """
    Returns all the data of an S-Expression Symbol matching given token.
    Example:    item = (user (name John) (surname Doe))
                token = user
                return (name John) (surname Doe)
    Example:    item = (user (name John) (surname Doe))
                token = name
                return 'John'
    """
    data = None
    if type(item) == list:
        for cons in item:
            if type(cons) == sexpdata.Symbol:
                if cons.value() == token:
                    data = sexpdata.cdr(item)
            elif type(cons) != sexpdata.Symbol and type(cons) == list:
                if recursive:
                    data = get_symbol_data_by_token(cons, token)
            if data is not None:
                break
    return data
