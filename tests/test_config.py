import pytest
from .tool import icludepath  # incule app path to be imported as app
from app import create_app
from app.config import DevelopmentConfig, TestingConfig

icludepath()


@pytest.fixture()
def app():
    app = create_app(DevelopmentConfig)
    yield app


@pytest.fixture()
def client(app):
    app.config.update(TestingConfig)
    return app.test_client()


@pytest.fixture()
def runner():
    app.config.update(DevelopmentConfig)
    return app.test_cli_runner()


if False:

    def test_logout_redirect(client):
        response = client.get("/logout")
        # Check that there was one redirect response.
        assert len(response.history) == 1
        # Check that the second request was to the index page.
        assert response.request.path == "/index"


def test_01(app):
    assert 1 == 1
