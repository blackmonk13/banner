from peewee import *

app_db = SqliteDatabase('app.db', pragmas={'journal_mode': 'wal'})


class BaseModel(Model):
    """A base model that will use our Sqlite database."""
    class Meta:
        database = app_db
