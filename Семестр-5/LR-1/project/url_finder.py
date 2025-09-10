from importlib.abc import PathEntryFinder
from importlib.util import spec_from_loader
from urlloader import URLLoader

class URLFinder(PathEntryFinder):
    def __init__(self, url: str, available: str):
        self.url = url
        self.available = available
        
    def find_spec(self, name: str, target=None):
        if name not in self.available:
            raise ImportError(f"Module {name} not found")

        origin = f"{self.url}/{name}.py"
        loader = URLLoader()
        return spec_from_loader(name, loader, origin=origin)            
