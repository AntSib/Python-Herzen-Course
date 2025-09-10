import sys
from urlhook import url_hook


if __name__ == "__main__":
    url = "https://antsib.github.io/remotemodule/myremotemodule.py"

    sys.path_hooks.append(url_hook)
    sys.path.append(url)

    from myremotemodule import myfoo

    myfoo()
