import os
import pathlib
from peewee import *

# Get the user's home directory
home_dir = pathlib.Path.home()

# Create a hidden folder called '.banner' inside the user's home directory
banner_data_dir = home_dir / '.banner'
banner_data_dir.mkdir(parents=True, exist_ok=True)

# Set the database file path inside the '.banner' folder
db_file_path = banner_data_dir / 'app.db'

app_db = SqliteDatabase(str(db_file_path), pragmas={'journal_mode': 'wal'})
class BaseModel(Model):
    """A base model that will use our Sqlite database."""
    class Meta:
        database = app_db
