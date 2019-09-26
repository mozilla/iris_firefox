import os
import sys

from moziris.api.settings import Settings
from moziris.scripts.main import main


def start():
    path = os.path.split(__file__)[0]
    sys.path.append(path)
    print(path)
    Settings.set_code_root_from_caller()
    main()
