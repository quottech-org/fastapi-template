from sqlalchemy import Column, BigInteger
from sqlalchemy.ext.declarative import declared_attr


class IDMixin:
    @declared_attr
    def id(cls):
        return Column(BigInteger, primary_key=True, autoincrement=True)
