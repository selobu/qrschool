from sys import path
from pathlib import Path
from os.path import abspath, join

# Add current path to sys.path
cp = Path(__file__).parent
if abspath(cp) not in path:
    path.append(abspath(cp))
