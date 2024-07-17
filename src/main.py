# coding: utf-8
__version__ = "0.1.0"

from app import create_app

app = create_app()
app.config
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081, debug=False)
