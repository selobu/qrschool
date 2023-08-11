__all__ = ["db", "Tb", "select", "uuidgenerator", "now", "Base"]
from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4
from datetime import datetime, timedelta
from sqlalchemy import select
from sqlalchemy.orm import class_mapper
from sqlalchemy.inspection import inspect
from flask import current_app as app, abort
from flask_jwt_extended import current_user, jwt_required
import hashlib
from functools import wraps

db = SQLAlchemy(
    engine_options={"pool_recycle": 280}, session_options={"autoflush": False}
)

authorizations = {"Bearer": {"type": "apiKey", "in": "header", "name": "Authorization"}}


def select(*args, **kwargs):
    return db.session.query(*args, **kwargs)


class TbContainer(object):
    pass


Tb = TbContainer()


def map_name_to_table(cls):
    """Decorator to map table names into the TbContainer"""
    if hasattr(Tb, cls.__name__):
        raise Exception(f"ya esta declarada la tabla {cls.__name__}")
    setattr(Tb, cls.__name__, cls)

    @staticmethod
    def register(**kwargs):
        commit = False
        if 'commit' in kwargs:
            commit = kwargs.pop('commit')
        primary_keys = class_mapper(cls).primary_key
        primary_key_names = []
        found_primary_key = False
        for primary_key in primary_keys:
            if primary_key.name in kwargs:
                found_primary_key = True
                primary_key_names.append(primary_key.name)
        if not found_primary_key:
            model = cls()
        else:
            # se busca para modificarlo
            with app.Session() as session:
                res = select(cls).filter_by(
                    **dict((primary_key_name, kwargs[primary_key_name]) \
                           for primary_key_name in primary_key_names))
                res = session.execute(res).all()
            if len(res) == 0:
                model = cls()
            else:
                model = res[0][0]
        for primary_key in primary_keys:
            if primary_key.name in kwargs:
                setattr(model, primary_key.name,
                        kwargs.pop(primary_key.name))
            # TODO check if the primary_key is required
        inspected = inspect(cls)
        columns = dict((fieldname, col)
                       for fieldname, col in cls.__table__.columns.items())
        for key, value in kwargs.items():
            if hasattr(model, key) and key in columns:
                # Se identifica si la columna es de tipo Date o DateTime
                if isinstance(columns[key].type, db.Date):
                    if isinstance(value, (str, bytearray)):
                        value = datetime.strptime(value, "%Y-%m-%d").date()
                elif isinstance(columns[key].type, db.DateTime):
                    if isinstance(value, (str, bytearray)):
                        # se trata de hacer la conversion del valor
                        posibleformats = ['%Y-%m-%dT%H:%M:%S.%fZ',
                                          '%Y-%m-%dT%H:%M:%S', '%Y-%m-%d %H:%M:%S']
                        for formato in posibleformats:
                            try:
                                value = datetime.strptime(value, formato)
                                break
                            except:
                                continue
                setattr(model, key, value)
            elif key not in columns:
                try:
                    relationitems = dict(
                        (key, value) for key, value in inspect(cls).relationships.items())
                except:
                    # db.session.rollback()
                    relationitems = []
                if key in relationitems:
                    # se consulta la llave foranea
                    table = relationitems[key].mapper
                    # solo se lee una llave primaria
                    filters = {}
                    _keys = [u.key for u in table.primary_key]
                    if len(_keys) == 1:
                        # se consulta la llave primaria
                        filters[_keys[0]] = value
                    else:
                        print(f'{key} - omititda. Basemodel no puede registrar multiples llaves')
                        continue
                    value = select(table).filter_by(**filters).one()
                    # select(getattr(tb)
                setattr(model, key, value)
            else:
                raise f"<{model.__table__.name}> Invalid parameter {key}"
        #db.session.add(model)
        #if commit:
        #    db.session.commit()
        return model
    if 'register' not in cls.__dict__:
        setattr(cls, 'register', register)
    else:
        setattr(cls, '_register', register)

    if 'delete' not in cls.__dict__:
        @staticmethod
        def delete(primary_key_value):
            # no se borra el proyecto solo se hace inactivo
            model = cls.query.get_or_404(primary_key_value)
            db.session.delete(model)
            try:
                db.session.commit()
            except:
                db.session.rollback()
                raise Exception(f'{model.__repr__} no se pudo eliminar')
        setattr(cls, 'delete', delete)

    def repr(self):
        primary_key = class_mapper(cls).primary_key[0].name
        return f'<{self.__tablename__} :>  {primary_key}: {getattr(self, primary_key)}'
    if 'function Model' in str(cls.__repr__):
        setattr(cls, '__repr__', repr)
    return cls

def uuidgenerator():
    return str(uuid4())


def now():
    return datetime.utcnow() - timedelta(hours=5)


from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


def gethash(password:str)->str:
    """Returns a hash value of the given password"""
    m= hashlib.sha256()
    m.update(bytes('Colegio2023!'+password,'utf-8'))
    m.digest()
    return m.hexdigest()


def is_admin():
    try:
        return current_user().rol == 1
    except:
        return False

@jwt_required()
def admin_required(proyectIdKeyName=None):
    def newadmin(func):
        @wraps(func)
        def func_wrapper(*args, **kwargs):
            proy = Tb.Proyecto.query.get_or_404(kwargs[proyectIdKeyName])
            if proy.isUserAdmin(current_user().id):
                return func(*args, **kwargs)
            abort(400, 'admin required')
        return func_wrapper
    return newadmin

@jwt_required()
def activeuser_required(proyectIdKeyName=None):
    def newadmin(func):
        @wraps(func)
        def func_wrapper(*args, **kwargs):
            proy = Tb.Proyecto.query.get_or_404(kwargs[proyectIdKeyName])
            currusr = current_user()
            if proy.isUserAdmin(currusr.id) or proy.isActiveUser(currusr.id):
                return func(*args, **kwargs)
            abort(400, 'active user required')
        return func_wrapper
    return newadmin