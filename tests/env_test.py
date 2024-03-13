from app.config import (
    ProductionConfig,
    DevelopmentConfig,
    TestingConfig,
    PythonAnywhereConfig,
)
import unittest
from pydantic import SecretStr


keys = [
    "API_NAME",
    "VERSION",
    "API_URL_PREFIX",
    "API_DESCRIPTION",
    "admin_email",
    "items_per_user",
    "API_CONTACT",
    "JWT_SECRET_KEY",
    "WTF_CSRF_SECRET_KEY",
    "app",
    "engine",
    "ECHO",
    "APP_NAME",
    "FLASK_ADMIN_SWATCH",
    "ADMIN_TEMPLATE_NAME",
    "TESTING",
    "PER_PAGE",
    "SQLALCHEMY_DATABASE_URI",
]
var_types = [
    str,
    str,
    str,
    str,
    str,
    int,
    object,
    str,
    str,
    object,
    object,
    bool,
    str,
    str,
    str,
    bool,
    int,
    str,
]


class TestConfig(unittest.TestCase):

    def test_env_var(self):
        conf = TestingConfig
        for variable, var_type in [
            ("user", str),
            ("JWT_SECRET_KEY", str),
            ("host", str),
            ("db", str),
            ("host", str),
            ("ECHO", bool),
            ("APP_NAME", str),
            ("pwd", SecretStr),
        ]:
            self.assertIsInstance(getattr(conf, variable), var_type)

    def test_config(
        self,
    ):
        conf = TestingConfig
        for key in keys:
            assert hasattr(conf, key)

    def test_config_type(
        self,
    ):
        conf = TestingConfig
        for key, var_type in zip(keys, var_types):
            self.assertIsInstance(getattr(conf, key), var_type)

    def test_production_config(
        self,
    ):
        conf = ProductionConfig
        self.assertTrue(conf.SQLALCHEMY_DATABASE_URI.startswith("mysql+pymysql:"))
        self.assertFalse(conf.ECHO)

    def test_development_config(self):
        conf = DevelopmentConfig
        self.assertTrue(conf.SQLALCHEMY_DATABASE_URI.startswith("sqlite:"))
        self.assertTrue(conf.ECHO)

    def test_testing_config(self):
        conf = TestingConfig
        self.assertEqual(conf.SQLALCHEMY_DATABASE_URI, "sqlite://:@:/:memory:")
        self.assertTrue(conf.ECHO)
        self.assertTrue(conf.TESTING)

    def test_pythonanywhere_conf(self):
        conf = PythonAnywhereConfig
        self.assertIsInstance(conf.db, str)
        self.assertIsInstance(conf.user, str)
        self.assertTrue(conf.host.endswith(".mysql.pythonanywhere-services.com"))
        username = conf.host.split(".")[0]
        self.assertEqual(username, conf.user)
        self.assertTrue(conf.db.startswith(f"{username}$"))
        self.assertTrue(conf.SQLALCHEMY_DATABASE_URI.startswith("mysql+pymysql://"))
        self.assertIn(username, conf.SQLALCHEMY_DATABASE_URI)
        self.assertTrue(conf.SQLALCHEMY_DATABASE_URI.endswith(conf.db))
