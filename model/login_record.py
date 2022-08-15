# -*- coding: utf-8 -*-
# @Time    : 2022/7/29 11:50 AM
# @Author  : Barin
# @FileName: login_record.py
# @Software: PyCharm

from sqlalchemy import Column, String, JSON
from sqlalchemy.dialects.mysql import INTEGER

from . import BaseModel, PanelBase


class LoginRecord(PanelBase, BaseModel):
    __tablename__ = 'login_record'

    loid = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    lo_status = Column(INTEGER, nullable=False, default=1)
    lo_token = Column(String(40), nullable=False)
    lo_usid = Column(INTEGER, nullable=False)

    lo_create = Column(INTEGER(unsigned=True), nullable=False)
    lo_update = Column(INTEGER(unsigned=True), nullable=False)
    lo_delete = Column(INTEGER(unsigned=True))