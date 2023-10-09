# coding: utf-8
__version__ = "0.1.0"

from app import create_app
from app.config import PythonAnywhereConfig

app = create_app(PythonAnywhereConfig)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8082, debug=True)
