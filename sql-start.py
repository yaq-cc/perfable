import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sql_models import User, Note, NoteCategory, NoteCollaborator, create_tables, drop_tables


class Sequence:

    def __init__(self, init: int = -1):
        self.val = init
    
    def __call__(self):
        self.val += 1
        return self.val


DB_CNST = os.environ.get("_DB_CNST")

engine = create_engine(DB_CNST)
Session = sessionmaker(engine)

# Recreate all the tables.
drop_tables(engine)
create_tables(engine)

with Session() as session:
    # Note categories
    note_cat_seq = Sequence()
    customer_success   = NoteCategory(note_category_id=note_cat_seq(), note_category_name="Customer Success")
    business           = NoteCategory(note_category_id=note_cat_seq(), note_category_name="Business (Sales Metrics)") 
    people             = NoteCategory(note_category_id=note_cat_seq(), note_category_name="People (Winning as One Team)")
    exceptional_impact = NoteCategory(note_category_id=note_cat_seq(), note_category_name="Exceptional Impact & Transformational Works")
    session.add(customer_success)
    session.add(business)
    session.add(people)
    session.add(exceptional_impact)
    session.commit()