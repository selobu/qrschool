from app.config import (
    adminuser,
    user,
    port,
    database,
    host,
    echo_value,
    appname,
    userpassword,
    adminpassword,
    jwt_key,
    Config,
    ProductionConfig,
    DevelopmentConfig,
    TestingConfig,
    PythonAnywhereConfig,
    hostpythonanywhere,
    databasepythonanywhere,
    userpythonanywhere,
)


def test_env_var():
    assert isinstance(adminuser, str)
    assert isinstance(user, str)
    assert isinstance(port, str)
    assert isinstance(database, str)
    assert isinstance(host, str)
    assert isinstance(database, str)
    assert isinstance(host, str)
    assert isinstance(echo_value, bool)
    assert isinstance(appname, str)
    assert isinstance(userpassword, str)
    assert isinstance(adminpassword, str)
    assert isinstance(jwt_key, str)


def test_config():
    conf = Config()
    assert hasattr(conf, "API_NAME")
    assert hasattr(conf, "VERSION")
    assert hasattr(conf, "API_URL_PREFIX")
    assert hasattr(conf, "API_DESCRIPTION")
    assert hasattr(conf, "admin_email")
    assert hasattr(conf, "items_per_user")
    assert hasattr(conf, "API_CONTACT")
    assert hasattr(conf, "JWT_SECRET_KEY")
    assert hasattr(conf, "WTF_CSRF_SECRET_KEY")
    assert hasattr(conf, "app")
    assert hasattr(conf, "engine")
    assert hasattr(conf, "ECHO")
    assert hasattr(conf, "APP_NAME")
    assert hasattr(conf, "FLASK_ADMIN_SWATCH")
    assert hasattr(conf, "ADMIN_TEMPLATE_NAME")
    assert hasattr(conf, "TESTING")
    assert hasattr(conf, "PER_PAGE")
    assert hasattr(conf, "SQLALCHEMY_DATABASE_URI")


def test_config_type():
    conf = Config()
    assert isinstance(conf.API_NAME, str)
    assert isinstance(conf.VERSION, str)
    assert isinstance(conf.API_URL_PREFIX, str)
    assert isinstance(conf.API_DESCRIPTION, str)
    assert isinstance(conf.admin_email, str)
    assert isinstance(conf.items_per_user, int)
    assert isinstance(conf.API_CONTACT, object)
    assert isinstance(conf.JWT_SECRET_KEY, str)
    assert isinstance(conf.WTF_CSRF_SECRET_KEY, str)
    assert isinstance(conf.app, object)
    assert isinstance(conf.engine, object)
    assert isinstance(conf.ECHO, bool)
    assert isinstance(conf.APP_NAME, str)
    assert isinstance(conf.FLASK_ADMIN_SWATCH, str)
    assert isinstance(conf.ADMIN_TEMPLATE_NAME, str)
    assert isinstance(conf.TESTING, bool)
    assert isinstance(conf.PER_PAGE, int)
    assert isinstance(conf.SQLALCHEMY_DATABASE_URI, str)


def test_production_config():
    conf = ProductionConfig()
    assert conf.SQLALCHEMY_DATABASE_URI.startswith("mysql+pymysql:")
    assert conf.ECHO is False


def test_development_config():
    conf = DevelopmentConfig()
    assert conf.SQLALCHEMY_DATABASE_URI.startswith("sqlite:")
    assert conf.ECHO is True


def test_testing_config():
    conf = TestingConfig()
    assert conf.SQLALCHEMY_DATABASE_URI == "sqlite:///:memory:"
    assert conf.ECHO is True
    assert conf.TESTING is True


def test_pythonanywhere_conf():
    conf = PythonAnywhereConfig()
    assert isinstance(hostpythonanywhere, str)
    assert isinstance(databasepythonanywhere, str)
    assert isinstance(userpythonanywhere, str)
    assert hostpythonanywhere.endswith(".mysql.pythonanywhere-services.com")
    username = hostpythonanywhere.split(".")[0]
    assert username == userpythonanywhere
    assert databasepythonanywhere.startswith(f"{username}$")
    assert conf.SQLALCHEMY_DATABASE_URI.startswith("mysql+pymysql://")
    assert username in conf.SQLALCHEMY_DATABASE_URI
    assert conf.SQLALCHEMY_DATABASE_URI.endswith(databasepythonanywhere)
