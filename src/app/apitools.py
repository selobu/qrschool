# coding:utf-8
__all__ = ["createApiModel"]
from typing import Any
from flask_restx import Model, fields, api
from flask import current_app
from sqlalchemy import types, select
from sqlalchemy.inspection import inspect
from functools import wraps
from flask_restx import reqparse
from dataclasses import dataclass

# api = current_app.api  # type: ignore

_not_allowed = ["TypeEngine", "TypeDecorator", "UserDefinedType", "PickleType"]
conversion = {
    "INT": "Integer",
    "CHAR": "String",
    "VARCHAR": "String",
    "NCHAR": "String",
    "NVARCHAR": "String",
    "TEXT": "String",
    "Text": "String",
    "FLOAT": "Float",
    "NUMERIC": "Float",
    "REAL": "Float",
    "DECIMAL": "Float",
    "TIMESTAMP": "DateTime",
    "DATETIME": "DateTime",
    "CLOB": "Raw",
    "BLOB": "Raw",
    "BINARY": "Raw",
    "VARBINARY": "Raw",
    "BOOLEAN": "Boolean",
    "BIGINT": "Integer",
    "SMALLINT": "Integer",
    "INTEGER": "Integer",
    "DATE": "Date",
    "TIME": "String",
    "String": "String",
    "Integer": "Integer",
    "SmallInteger": "Integer",
    "BigInteger": "Integer",
    "Numeric": "Float",
    "Float": "Float",
    "DateTime": "DateTime",
    "Date": "Date",
    "Time": "String",
    "LargeBinary": "Raw",
    "Boolean": "Boolean",
    "Unicode": "String",
    "Concatenable": "String",
    "UnicodeText": "String",
    "Interval": "List",
    "Enum": "List",
    "Indexable": "List",
    "ARRAY": "List",
    "JSON": "List",
}

fieldtypes = [
    r
    for r in dir(types)
    if (r not in _not_allowed) and (not r.startswith("_")) and r[0] == r[0].upper()
]


def _get_res(
    table, modelname: str = None, readonlyfields: list = [], show: list = []
) -> Model:
    """Private function to obtain model_columns as a list
    Args:
        table: SQLalchemy Table
        modelname (Optional[str], optional): Custom model name. if it's is None then the modelname will be the capitalized tablename.
        readonlyfields (Optional[list], optional): Set readonly fields. Defaults to [].
        show (Optional[list], optional): Set shown fields. Defaults to [].
    Return:
        Model
    """

    res = {}
    foreignsmapped = []
    # reading from sqlalchemy column into flask-restx column
    for fieldname, col in table.__table__.columns.items():
        tipo = col.type
        isprimarykey = col.primary_key and fieldname not in show
        params = {}
        fieldnameinreadonly = fieldname in readonlyfields
        if isprimarykey or fieldnameinreadonly:
            params = {"readonly": True}
        if not col.nullable and (not fieldnameinreadonly) and (not isprimarykey):
            params["required"] = True
        if col.default is not None:
            # if isinstance(col.default.arg, (str, float, int, bytearray, bytes)):
            params["default"] = col.default.arg
        _tipo = str(tipo).split("(")[0]
        if _tipo in fieldtypes:
            if hasattr(tipo, "length"):
                params["max_length"] = tipo.length
            if len(col.foreign_keys) > 0:
                foreignsmapped.extend(list(col.foreign_keys))
            res[fieldname] = getattr(fields, conversion[_tipo])(**params)
    # cheking for relationships
    relationitems = []
    # try:
    relationitems = inspect(table).relationships.items()
    # except:
    # It could faild in composed primary keys
    #    pass
    # implementing relationship columns
    for field, relationship in relationitems:
        if relationship.backref != table.__tablename__:
            continue
        try:
            col = list(relationship.local_columns)[0]
            tipo = col.type
            _tipo = str(tipo).split("(")[0]
            if _tipo in fieldtypes:
                outparams = {}
                if hasattr(tipo, "length"):
                    params["max_length"] = tipo.length
                if field in readonlyfields:
                    outparams["readonly"] = True
                if col.foreign_keys is not None:
                    foreignsmapped.extend(list(col.foreign_keys))
                if relationship.uselist:
                    res[field] = fields.List(
                        getattr(fields, conversion[_tipo])(**params), **outparams
                    )
                else:
                    for key, value in outparams.items():
                        params[key] = value
                    res[field] = getattr(fields, conversion[_tipo])(**params)
        except Exception:
            continue
    if modelname in ("", None):
        modelname = table.__tablename__.lower().capitalize()
    return res


def get_model_list(model: Model, limit: int = 50):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with current_app.Session() as session:
                res = select(model).limit(limit)
                items = session.scalars(res).all()
                return items

        return wrapper

    return decorator


def post_model_list(payload: str, model: Model):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            modellist = api.payload[payload]
            # Session.begin() set automatically the commit once it takes out the with statement
            with current_app.Session() as session:
                res = [model.register(**mod) for mod in modellist]
                session.add_all(res)
                session.commit()
            return res

        return wrapper

    return decorator


def get_model(model: Model):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with current_app.Session() as session:
                res = select(model).filter_by(**kwargs)
                item = session.scalars(res).one()
            return item

        return wrapper

    return decorator


def put_model(model: Model):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Session.begin() set automatically the commit once it takes out the with statement
            data = api.payload
            with current_app.Session() as session:
                res = model.register(**kwargs, **data)
                session.add(res)
                session.commit()
            return res

        return wrapper

    return decorator


def createApiModel(
    api: api,
    table,
    modelname: str = None,
    readonlyfields: list = [],
    show: list = [],
    additionalfields: dict = {},
) -> Model:
    """Create a basic Flask-restx ApiModel by given an sqlachemy Table and a flask-restx api.
    Requires sqlalchemy

    Args:
        api: Flask-restx api
        table: SqlalchemyTable
        modelname (Optional[str], optional): Custom model name. if it's is None then the modelname will be the capitalized tablename.
        readonlyfields (Optional[list], optional): Set readonly fields. Defaults to [].
        show (Optional[list], optional): Set shown fields. Defaults to [].

    Return:
        Model
    """
    res = _get_res(table, modelname, readonlyfields, show)
    if len(additionalfields) > 0:
        # adding more fields
        for key, value in additionalfields.items():
            if key in res:
                continue
            res[key] = value
    return api.model(modelname, res)


@dataclass
class Argument:
    name: str
    type: object
    help: str
    required: bool


class ParserModel:
    _paginate_model = None
    __args: dict = {}

    def add_argument(self, Argument: Argument):
        self.__add_argument(
            name=Argument.name,
            type=Argument.type,
            help=Argument.help,
            required=Argument.required,
        )
        return self

    def __add_argument(self, name: str, type=object, help=str, required=bool):
        self.paginate_model.add_argument(name, type=type, help=help, required=required)
        self.__parsed = False
        return self

    def add_paginate_arguments(self):
        self.add_argument(
            Argument(
                name="page",
                type=int,
                help="Page to visualize - optional",
                required=False,
            )
        )
        self.add_argument(
            Argument(
                name="per_page",
                type=int,
                help="Maximum results per page - optional",
                required=False,
            )
        )
        return self

    @property
    def paginate_model(self):
        if self._paginate_model is None:
            self._paginate_model = reqparse.RequestParser()
        return self._paginate_model

    @property
    def args(self):
        if self.__parsed is None:
            self.__args = self.__parse_args()
        return self.__args

    def __parse_args(self):
        self.__args = self._paginate_model.parse_args()
        self.__parsed = True
        return self.__args

    def __getitem__(self, __name: str) -> Any:
        if not self.__parsed:
            self.__parse_args()
        if __name not in self.__args:
            return IndexError("Element not found!")

    def get(self, Argument, default=None):
        if Argument not in self.args:
            return default
        if (param := self.args[Argument]) is None:
            param = default
        return param


parser = ParserModel().add_paginate_arguments()
paginate_model = parser.paginate_model
