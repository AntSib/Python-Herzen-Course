import sys
from urlhook import url_hook


if __name__ == "__main__":
    url = "http://localhost:8000/"

    sys.path_hooks.append(url_hook)
    sys.path.append(url)

    from myremotemodule import myfoo

    myfoo()
