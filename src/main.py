# coding: utf-8
__version__ = "0.1.0"
from flask_cors import CORS

from app import create_app

app = create_app()

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


if __name__ == "__main__":
    app.run(port=8081, debug=False)
