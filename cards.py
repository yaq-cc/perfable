import json

from chat.events import Event
from chat.messages import Card, CardHeader, Widget, Section, CardAction
from chat.messages import ActionResponse, ActionResponseTypes, DialogAction, Dialog, ActionStatus  
from chat.messages import DecoratedText, Icon, TextInput, TextInputTypes, Suggestions, SuggestionItem
from chat.messages import SelectionInput, SelectionItem, SelectionType
from chat.messages import DateTimePicker, DateTimePickerType
from chat.messages import ButtonList, Button, OnClick, Action
from sql_models import User, NoteCategory, Note, NoteCollaborator

# https://developers.googleblog.com/2021/06/add-dialogs-and-slash-commands-to-your-google-workspace-chat-bots.html

def new_note_dialog(event: Event) -> Card:
    
    user = event.state.get("user")
    session = event.state.get("session")

    user_widget = Widget(decoratedText=DecoratedText(
        topLabel="User",
        text=user.user_display_name,
        startIcon=Icon(altText="This is you", knownIcon="PERSON", imageType="SQUARE")
    ))

    perf_period = Widget(selectionInput=SelectionInput(
        type=SelectionType.DROPDOWN,
        name="perf_period", 
        label="Perf Period",
        items=[
            SelectionItem(text="My text", value="yup", selected=False),
            SelectionItem(text="My other text", value="other")
        ]
    ))

    activity_date = Widget(dateTimePicker=DateTimePicker(
        label="Activity Date",
        name="activity_date",
        type=DateTimePickerType.DATE_ONLY,
        valueMsEpoch=DateTimePicker.now(),
    ))

    categories = NoteCategory.list_categories(session)
    items = [
        SelectionItem(
            text=category.note_category_name,
            value=str(category.note_category_id),
        ) for category in categories
    ]

    perf_category = Widget(selectionInput=SelectionInput(
        type=SelectionType.DROPDOWN,
        name="perf_category", 
        label="Perf Category",
        items=items,
    ))
    
    note_description = Widget(textInput=TextInput(
        label="Describe your impactful activity",
        type=TextInputTypes.SINGLE_LINE,
        name="note_description",
    ))

    note_value = Widget(textInput=TextInput(
        label="Financial Imapct",
        type=TextInputTypes.SINGLE_LINE,
        name="note_value",
    ))

    note_salesforce_id = Widget(textInput=TextInput(
        label="Related Vector Opportunity Link",
        type=TextInputTypes.SINGLE_LINE,
        name="note_salesforce_id",
    ))

    note_collaborators = Widget(textInput=TextInput(
        label="Activity Collaborators",
        type=TextInputTypes.SINGLE_LINE,
        name="note_collaborators",
        hintText="comma separated listing of collaborator LDAPs"
    ))

    submit_action = Action(function="newNoteSubmit")
    cancel_action = Action(function="newNoteCancel")

    submit_buttons = Widget(buttonList=ButtonList(
        buttons=[
            Button(text="Submit", onClick=OnClick(action=submit_action)),
            Button(text="Cancel", onClick=OnClick(action=cancel_action)),
        ]
    ))

    widgets = [
        user_widget,
        perf_period,
        activity_date,
        perf_category,
        note_description,
        note_value,
        note_salesforce_id,
        note_collaborators,
        submit_buttons
    ]

    card = Card(
        name="my-dialog-card",
        sections=[
            Section(widgets=widgets)
        ],
    )

    return ActionResponse.make(
        type=ActionResponseTypes.DIALOG,
        dialogAction=DialogAction(
            dialog=Dialog(body=card),
        ),
    )


