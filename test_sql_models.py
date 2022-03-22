import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sql_models import NoteCategory

# Reserved for database configuration
DB_HOST = os.environ.get("_DB_HOST")
DB_PORT = os.environ.get("_DB_PORT")
DB_USER = os.environ.get("_DB_USER")
DB_PASS = os.environ.get("_DB_PASS")
DB_NAME = os.environ.get("_DB_NAME")
DB_CNST = os.environ.get("_DB_CNST") # DB_CNST = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Database engine and session objects
engine = create_engine(DB_CNST)
Session = sessionmaker(engine)

with Session() as session:
    categories = NoteCategory.list_categories(session)
    for cat in categories:
        print(cat.note_category_name)