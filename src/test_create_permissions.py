from app import create_app
from app.shellcontex.whatnext import whatsnext

app = create_app()

with app.app_context():
    whatsnext()
