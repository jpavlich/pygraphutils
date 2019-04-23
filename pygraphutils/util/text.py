import re


def standardize_string(s: str):
    """ Removes duplicate spaces, remove surrounding spaces and converts to lowercase
    
    Arguments:
        s {str} -- [description]
    
    Returns:
        [type] -- [description]
    """
    if isinstance(s, str):
        s = re.sub(r"\s+", " ", s)
        s = s.strip().lower().title()
    return s
