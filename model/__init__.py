from typing import List, Dict
from pprint import pprint
from collections import namedtuple

from sqlalchemy import create_engine, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.query import Query

from util.time import now

PanelBase = declarative_base()
PanelSession = scoped_session(sessionmaker())


class BaseModel(object):
    __service__ = 'panel'
    query: Query = None

    @classmethod
    def new(cls, **info):

        table = cls.__tablename__
        prefix = f"{table.lower()[:2]}_"

        new_info = {}
        for key, val in info.items():
            if val is None:
                continue
            if not prefix in key:
                key = f"{prefix}{key}"
            new_info[key] = val
        create_key = f"{prefix}create"
        update_key = f"{prefix}update"
        status_key = f"{prefix}status"
        if hasattr(cls, create_key):
            new_info.setdefault(create_key,now())
        if hasattr(cls, update_key):
            new_info.setdefault(update_key, now())
        if hasattr(cls, status_key):
            new_info.setdefault(status_key, 1)
        return cls(**new_info)

    def as_dict(self) -> Dict:
        prefix = self.__tablename__[:2]
        attrs = dir(self)
        info = {}
        for attr in attrs:
            if not prefix in attr:
                continue
            info[attr] = getattr(self, attr)
        return info

    def update(self, **kwargs):
        prefix = self.__tablename__[:2] + "_"
        update_key = f'{prefix}update'
        if hasattr(self, update_key):
            setattr(self, update_key, now())

        for key, val in kwargs.items():
            if prefix not in key:
                key = f'{prefix}{key}'
            if val is None:
                continue
            if hasattr(self, key):
                setattr(self, key, val)
    
    @classmethod
    def GeometryQurery(cls, geometry=None, exclude=None):
        if not geometry:
            return
        prefix = cls.__tablename__[:2]
        fields = [getattr(cls, attr) for attr in dir(cls)
            if attr not in (exclude or []) and attr.startswith(prefix)
        ]

        query = cls.query.with_entities(
            *fields,
            func.st_asgeojson(getattr(cls, geometry))
        )
        return query
    
    
    @classmethod
    def as_objects(cls, data, exclude=None, geometry=None):
        if not data:
            return []

        if not geometry:
            return 

        prefix = cls.__tablename__[:2]
        fields = [attr for attr in dir(cls) 
            if attr not in (exclude or []) and attr.startswith(prefix)
        ]
        new = namedtuple(
            'New{0}'.format(cls.__name__), 
            [*fields, 're_{0}'.format(geometry)]
        )
        if isinstance(data[0], tuple) or isinstance(data[0], list):
            return [new(*row) for row in data]
        else:
            return new(*data)


BaseModel.query = PanelSession.query_property()


def init_panel_session(engine):
    PanelSession.configure(bind=engine)


from .user import User

from .login_record import LoginRecord