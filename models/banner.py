from peewee import *
from .base import BaseModel


class Banner(BaseModel):
    id = AutoField(primary_key=True)
    content = TextField()
    markedUp = TextField(null=True)
