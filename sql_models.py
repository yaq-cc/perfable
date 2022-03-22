import uuid
from datetime import datetime

import psycopg2
from sqlalchemy import Integer, Column, create_engine, ForeignKey, String, select, DateTime
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base

from chat import models 

def guid():
    return str(uuid.uuid4())

def now():
    return datetime.now()

def easy_id():
    return "random-string"

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    user_id = Column(String, primary_key=True, default=guid)
    user_email = Column(String)
    user_name = Column(String)
    user_created = Column(DateTime, default=now)
    user_display_name = Column(String)
    user_first = Column(String)
    user_last = Column(String)

    @staticmethod
    def get_user(session: Session, user: models.User):
        # Returns None if no user is found.
        print("getting user.")
        return (
            session
                .query(User)
                .filter(User.user_email == user.email)
                .first()
        )

    @staticmethod
    def create_user(session: Session, user: models.User):
        print("Setting user.")
        username, domain = user.email.split("@")
        name_parts = user.senders_name
        mappings = dict(
            user_email=user.email,
            user_name=username,
            user_display_name=user.displayName,
            user_first=name_parts[0],
            user_last=name_parts[-1]
        )
        _user = User(**mappings)
        session.add(_user)
        session.commit()
        return _user

    @staticmethod
    def get_or_create_user(session: Session, user: models.User):
        _user = User.get_user(session, user)
        if not _user:
            _user = User.create_user(session, user)
        return _user


class NoteCategory(Base):
    __tablename__ = "note_categories"
    note_category_id = Column(Integer, primary_key=True)
    note_category_name = Column(String)
    note_category_description = Column(String)
    note_category_created = Column(DateTime, default=now)

    @staticmethod
    def list_categories(session: Session):
        return (
            session
                .query(NoteCategory)
                .all()
        )


class Note(Base):
    __tablename__ = "notes"
    note_id = Column(String, primary_key=True, default=guid)
    # ForeignKey("users.user_id")
    note_owner = Column(String, ForeignKey(User.user_id))
    note_easy_id = Column(String, default=easy_id)
    note_perf_period = Column(String)
    note_index = Column(Integer)
    # ForeignKey("note_categories.note_category_id")
    note_category = Column(Integer, ForeignKey(NoteCategory.note_category_id))
    note_description = Column(String)
    note_value  = Column(Integer)
    note_salesforce_id = Column(String)
    note_created = Column(DateTime, default=now)
    note_last_modified = Column(DateTime, default=now)

    def create_note(self, session: Session):
        session.add(self)
        session.commit()
        return self


class NoteCollaborator(Base):
    __tablename__ = "note_collaborators"
    note_collaborator_id = Column(String, primary_key=True, default=guid)
    # ForeignKey("notes.note_id")
    note_id = Column(String, ForeignKey(Note.note_id))
    # ForeignKey("users.user_id")
    note_collaborator_user_id = Column(String, ForeignKey(User.user_id))
    note_collaborator_created = Column(DateTime, default=now)


def create_tables(engine):
    return Base.metadata.create_all(engine)

def drop_tables(engine):
    return Base.metadata.drop_all(engine)