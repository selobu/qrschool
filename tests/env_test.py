from app.config import (
    ProductionConfig,
    DevelopmentConfig,
    TestingConfig,
    PythonAnywhereConfig,
    getData,
)
import unittest
from pydantic import SecretStr


keys = {
    "API_NAME": str,
    "VERSION": str,
    "API_URL_PREFIX": str,
    "API_DESCRIPTION": str,
    "admin_email": str,
    "items_per_user": int,
    "API_CONTACT": object,
    "JWT_SECRET_KEY": str,  # SecretStr,
    "WTF_CSRF_SECRET_KEY": str,  # SecretStr,
    "app": object,
    "engine": object,
    "ECHO": bool,
    "APP_NAME": str,
    "FLASK_ADMIN_SWATCH": str,
    "ADMIN_TEMPLATE_NAME": str,
    "TESTING": bool,
    "PER_PAGE": int,
    "SQLALCHEMY_DATABASE_URI": str,
}


class TestConfig(unittest.TestCase):

    def test_getData(self):
        pwd = getData("db_password.txt", "PWD", "password")
        self.assertGreater(len(pwd), 4)

        pwd = getData("db_password", "PWD", "")
        self.assertLess(len(pwd), 2)

    def test_env_var(self):
        conf = TestingConfig
        for variable, var_type in [
            ("user", str),
            ("JWT_SECRET_KEY", str),  # SecretStr),
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
        for key, var_type in keys.items():
            self.assertIsInstance(getattr(conf, key), var_type)

    def test_production_config(
        self,
    ):
        conf = ProductionConfig
        self.assertTrue(conf.SQLALCHEMY_DATABASE_URI.startswith("mysql+pymysql:"))
        self.assertFalse(conf.ECHO)

    def test_development_config(self):
        conf = DevelopmentConfig
        self.assertTrue(conf.SQLALCHEMY_DATABASE_URI.startswith("mysql+pymysql:"))
        self.assertTrue(conf.ECHO)

    def test_testing_config(self):
        conf = TestingConfig
        self.assertEqual(conf.SQLALCHEMY_DATABASE_URI, "sqlite:///:memory:")
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
