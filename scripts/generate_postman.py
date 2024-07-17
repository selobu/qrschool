from flask import json
from pathlib import Path
from sys import path as syspath

cpath = Path(__file__).parent.parent

if (pth := str(cpath / "src")) not in syspath:
    syspath.append(pth)

from app import create_app, config  # noqa:E402

Devconfig = config.DevelopmentConfig
Devconfig.SERVER_NAME = "localhost"

app = create_app(Devconfig)
with app.app_context():
    urlvars = False  # Build query strings in URLs
    swagger = True  # Export Swagger specifications
    data = app.api.as_postman(urlvars=urlvars, swagger=swagger)
    jsonfile = str(Path(__file__).parent / "postman.json")
    with open(jsonfile, "w") as fopen:
        fopen.write(
            json.dumps(data, indent=4).replace("http://localhost/api", r"{{api}}")
        )
        print(jsonfile)
