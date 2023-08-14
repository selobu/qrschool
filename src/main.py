# coding: utf-8
__version__ = "0.1.0"
from flask_cors import CORS

from app import create_app
from app.toolsapk import Base

app = create_app()


# needs to be called outside this cicle and just run once.
def createdb(engine):
    Base.metadata.create_all(engine)


createdb(app.engine)

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


if __name__ == "__main__":
    app.run(port=8081, debug=False)
