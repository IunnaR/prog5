from importlib.abc import PathEntryFinder
from importlib.util import spec_from_loader
import re
import sys
import request

class URLFinder(PathEntryFinder):
    def __init__(self, url, available):
        self.url = url
        self.available = available

    def find_spec(self, name, target=None):
        if name in self.available:
            origin = "{}/{}.py".format(self.url, name)
            loader = URLLoader()
            return spec_from_loader(name, loader, origin=origin)

        else:

            return None


class URLLoader:
    def create_module(self, target):
        return None

    def exec_module(self, module):
        source = requests.get(module.__spec__.origin).text
        code = compile(source, module.__spec__.origin, mode="exec")
        exec(code, module.__dict__)


def url_hook(some_str):
    if not some_str.startswith(("http", "https")):
        raise ImportError
    data = requests.get(some_str).text
    filenames = re.findall("[a-zA-Z_][a-zA-Z0-9_]*.py", data)
    modnames = {name[:-3] for name in filenames}
    return URLFinder(some_str, modnames)


sys.path_hooks.append(url_hook)

print(sys.path_hooks)
