# coding: utf-8
__version__ = "0.1.0"

from app import create_app
from app.config import ProductionConfig

app = create_app(ProductionConfig)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8082, debug=True)
