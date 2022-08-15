from sqlalchemy import Column, String, JSON
from sqlalchemy.dialects.mysql import INTEGER

from . import BaseModel, PanelBase


class User(PanelBase, BaseModel):
    __tablename__ = 'user'

    usid = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    us_status = Column(INTEGER, nullable=False, default=1)
    us_level = Column(INTEGER, nullable=False, default=1)
    us_name = Column(String(64), nullable=False)
    us_salt = Column(String(64), nullable=False)
    us_password = Column(String(64), nullable=False)

    us_create = Column(INTEGER(unsigned=True), nullable=False)
    us_update = Column(INTEGER(unsigned=True), nullable=False)
    us_delete = Column(INTEGER(unsigned=True))


