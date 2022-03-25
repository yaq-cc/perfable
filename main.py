import os
import json

import requests
from fastapi import FastAPI, Request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from chat.events import Event, EventTypes, TextResponse
from chat.messages import ActionResponse, ActionResponseTypes
from chat.messages import DialogAction, ActionStatus, ActionStatusCodes
from sql_models import User, NoteCategory, Note, NoteCollaborator
from cards import new_note_dialog

AUDITOR = "https://webhook.site/b1ed04dc-946b-42b4-b9f2-a62ef2d3cac4"
# https://perfable-63ietzwyxq-uk.a.run.app

# Reserved for database configuration
DB_HOST = os.environ.get("_DB_HOST")
DB_PORT = os.environ.get("_DB_PORT")
DB_USER = os.environ.get("_DB_USER")
DB_PASS = os.environ.get("_DB_PASS")
DB_NAME = os.environ.get("_DB_NAME")
# DB_CNST = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
DB_CNST = os.environ.get("_DB_CNST") 

# Database engine and session objects
engine = create_engine(DB_CNST)
Session = sessionmaker(engine)

app = FastAPI()

def dialog_event_router(event: Event):
    commandId = event.message.slashCommand.commandId
    card_response = new_note_dialog(event)
    print(json.dumps(card_response.to_dict()))
    return card_response

def slash_command_router(event: Event):
    commandId = event.message.slashCommand.commandId

    if event.isDialogEvent:
        return dialog_event_router(event)
    elif commandId == "1":
        user = event.state.get("user")
        print(user.user_display_name, " ~ ", user.user_id)
        note = Note(
            note_owner=user.user_id,
            note_perf_period="2022-H2",
            note_category=0,
            note_description="My very first note.",
            note_value=20000,  
        )
        note.create_note(event.state.get("session"))
        text = "slashCommand 1"
    elif commandId == "2":
        text = "slashCommand 2"
    elif commandId == "3":
        text = "slashCommand 3"
    elif commandId == "4":
        text = "slashCommand 4"
    else:
        text = "SlashCommand greater than 4!"

    return TextResponse(text=text)

def card_clicked_router(event: Event):
    if event.dialogEventType == "SUBMIT_DIALOG":
       if event.action.actionMethodName == "newNoteSubmit":
           print(json.dumps(event.common.formInputs, indent=2))
    else:
        print("NotImplementedError")

    response = ActionResponse.make(
        type=ActionResponseTypes.DIALOG,
        dialogAction=DialogAction(
            actionStatus=ActionStatus(
                statusCode=ActionStatusCodes.OK,
                userFacingMessage="Here's a message for you!",
            )
        ),
    )

    return response

def router(event: Event):

    # Check for the user.
    with Session() as session:
        user = User.get_or_create_user(session, event.user)
        event.update(dict(user=user, session=session))
    
    if event.type == EventTypes.ADDED_TO_SPACE:
        response = TextResponse(text=f"Hi {user.user_first}, nice to meet you albeit virtually. How can I help?")
    elif event.type == EventTypes.REMOVED_FROM_SPACE:
        response = TextResponse(text=f"Sorry to see you leave {user.user_first}.  Let's catch up soon!")
    elif event.type == EventTypes.CARD_CLICKED:
        response = card_clicked_router(event)
    elif event.type == EventTypes.MESSAGE:
        if event.message.slashCommand:
            response = slash_command_router(event)
        else:
            response = TextResponse(text="Talking to you sure is fun..!")
    return response.to_dict()

@app.post("/")
async def handler(request: Request):
    # Request.json is a coroutine and needs to be awaited.
    body = await request.json() 
    requests.post(AUDITOR, json=body)
    event = Event(**body)
    return router(event)

