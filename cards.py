import json

from chat.models import Event
from chat.models import Card, CardHeader, Section, CardAction, Icon
from chat.models import ActionResponse, ActionResponseTypes, DialogAction, Dialog, ActionStatus  
from chat.models import DecoratedText, TextInput, TextInputTypes
from chat.models import SelectionInput, SelectionItem, SelectionType
from chat.models import DateTimePicker, DateTimePickerType
from sql_models import User, NoteCategory, Note, NoteCollaborator

# https://developers.googleblog.com/2021/06/add-dialogs-and-slash-commands-to-your-google-workspace-chat-bots.html

def new_note_dialog(event: Event) -> Card:
    
    user = event.state.get("user")
    session = event.state.get("session")

    user_widget = DecoratedText.make(
        topLabel="User",
        text=user.user_display_name,
        startIcon=Icon(altText="This is you", knownIcon="PERSON", imageType="SQUARE")
    )

    perf_period = SelectionInput.make(
        type=SelectionType.DROPDOWN,
        name="perf_period", 
        label="Perf Period",
        items=[
            SelectionItem(text="My text", value="yup", selected=False),
            SelectionItem(text="My other text", value="other")
        ]
    )

    activity_date = DateTimePicker.make(
        label="Activity Date",
        name="activity_date",
        type=DateTimePickerType.DATE_ONLY,
        valueMsEpoch=DateTimePicker.now(),
    )

    categories = NoteCategory.list_categories(session)
    items = [
        SelectionItem(
            text=category.note_category_name,
            value=str(category.note_category_id),
        ) for category in categories
    ]

    perf_category = SelectionInput.make(
        type=SelectionType.DROPDOWN,
        name="perf_category", 
        label="Perf Category",
        items=items,
    )
    
    note_description = TextInput.make(
        label="Describe your impactful activity",
        type=TextInputTypes.SINGLE_LINE,
        name="note_description",
    )

    note_value = TextInput.make(
        label="Financial Imapct",
        type=TextInputTypes.SINGLE_LINE,
        name="note_value",
    )

    widgets = [
        user_widget,
        perf_period,
        activity_date,
        perf_category,
        note_description,
        note_value
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


