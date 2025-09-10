import re
import requests
from url_finder import URLFinder


def url_hook(some_str: str) -> object:
    """Return a finder object for remote modules at given URL.

    Downloads the directory listing from the given URL and looks for
    .py files. The names of those files (without .py) are used as module
    names. The finder object is then returned.

    If the URL is invalid or downloading fails for any reason, program
    exits with error message.

    Args:
        some_str (str): URL
    
    Returns:
        object: URLFinder

    """
    if not some_str.startswith(("http", "https")):
        raise ImportError("Not a valid URL")

    try:
        responce = requests.get(some_str, timeout=2)
        responce.raise_for_status()
    except requests.exceptions.ConnectionError as e:
        raise ImportError(f"Failed to fetch module from {some_str}: {e}")

    data = responce.text
    print(data)

    filenames = re.findall("[a-zA-Z_][a-zA-Z0-9_]*.py", data)
    modnames = {name[:-3] for name in filenames}

    return URLFinder(some_str, modnames)

