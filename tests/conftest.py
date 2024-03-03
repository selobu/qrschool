import pytest
from .tool import icludepath  # incule app path to be imported as app
from app import create_app
from app.config import DevelopmentConfig

icludepath()


@pytest.fixture
def app():
    app = create_app(DevelopmentConfig)
    app.config.update(TESTING=True)
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner():
    app.config.update(DevelopmentConfig)
    return app.test_cli_runner()


if False:

    def test_request_example(client):
        response = client.get("/posts")
        assert (
            b"<!doctype html>\n<html lang=en>\n<title>404 Not Found</title>\n<h1>Not Found</h1>\n<p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.</p>\n"
            in response.data
        )

    def test_logout_redirect(client):
        response = client.get("/logout")
        # Check that there was one redirect response.
        assert len(response.history) == 1
        # Check that the second request was to the index page.
        assert response.request.path == "/index"
