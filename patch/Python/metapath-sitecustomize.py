import os
import re
import sys
from importlib.abc import MetaPathFinder
from importlib.machinery import EXTENSION_SUFFIXES, ExtensionFileLoader
from importlib.util import spec_from_loader
from pathlib import Path

Frameworks_loc = Path(sys.executable).parent / "Frameworks"

filename_extension = [x for x in EXTENSION_SUFFIXES if bool(re.search(r"\.cpython.*dylib", x))][0]


class MyMetaPathFinder(MetaPathFinder):
    def find_spec(self, fullname, path, target=None):
        name = fullname.split(".")[-1]
        file_abs_path = os.path.join(Frameworks_loc, name + ".framework", name + filename_extension)

        if os.path.exists(file_abs_path):
            loader = ExtensionFileLoader(fullname, file_abs_path)
            return spec_from_loader(fullname, loader)
        else:
            return None


sys.meta_path.append(MyMetaPathFinder())
