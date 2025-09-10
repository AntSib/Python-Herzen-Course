import requests

class URLLoader:
    def create_module(self, target: str):
        return None
    
    def exec_module(self, module: str):
        responce = requests.get(module.__spec__.origin, timeout=2)
        source = responce.text

        code = compile(source, module.__spec__.origin, mode="exec")
        exec(code, module.__dict__)
