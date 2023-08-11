__all__ = ["icludepath"]

from sys import path as syspath
from pathlib import Path
from os.path import abspath


def icludepath():
    # Add current path to sys.path
    cp = Path(__file__).parent.parent
    cp = cp.joinpath('src')
    if abspath(cp) not in syspath:
        syspath.append(abspath(cp))
    print(cp)
    
icludepath()