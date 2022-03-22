import time

from typing import Optional, List, Union
from pydantic import BaseModel

# https://developers.google.com/chat/how-tos/cards-onclick
# https://developers.google.com/chat/api/reference/rest

# https://developers.googleblog.com/2021/06/add-dialogs-and-slash-commands-to-your-google-workspace-chat-bots.html
# https://gw-card-builder.web.app/

class User(BaseModel):
    name: str
    displayName: str
    avatarUrl: str
    email: str
    type: str
    domainId: str

    @property
    def senders_name(self):
        return self.displayName.split(" ")


class Sender(BaseModel):
    name: str
    displayName: str
    avatarUrl: str
    email: str
    type: str
    domainId: str


class Space(BaseModel):
    name: str
    type: str
    singleUserBotDm: bool
    spaceThreadingState: str
    spaceType: str
    spaceHistoryState: str


class RetentionSettings(BaseModel):
    state: str


class Thread(BaseModel):
    name: str
    retentionSettings: RetentionSettings


class Bot(BaseModel):
    name: str
    displayName: str
    avatarUrl: str
    type: str


class SlashCommand(BaseModel):
    bot: Optional[Bot]
    type: Optional[str]
    commandName: Optional[str]
    commandId: str
    triggersDialog: Optional[bool]


class Annotation(BaseModel):
    type: str
    startIndex: int
    length: int
    slashCommand: Optional[SlashCommand]


class Message(BaseModel):
    name: str
    sender: Sender
    createTime: str
    text: str
    annotations: Optional[List[Annotation]]
    thread: Thread
    space: Space
    argumentText: Optional[str]
    slashCommand: Optional[SlashCommand]
    lastUpdateTime: str


class Event(BaseModel):
    type: str
    eventTime: str
    message: Optional[Message]
    user: User
    space: Space
    configCompleteRedirectUrl: Optional[str]
    isDialogEvent: Optional[bool]
    dialogEventType: Optional[str]
    state: Optional[dict] = {}

    def update(self, data: dict):
        self.state.update(data)


class EventTypes:

    ADDED_TO_SPACE = "ADDED_TO_SPACE"
    MESSAGE = "MESSAGE"
    REMOVED_FROM_SPACE = "REMOVED_FROM_SPACE"
    CARD_CLICKED = "CARD_CLICKED"


class ToDictMixin(BaseModel):

    def to_dict(self):
        return self.dict(exclude_none=True)


class TextResponse(ToDictMixin, BaseModel):
    text: str


# https://developers.google.com/chat/api/reference/rest/v1/cards

class CardHeader(BaseModel):
    title: str
    subtitle: Optional[str]
    imageStyle: Optional[str]
    imageUrl: Optional[str]

class OnClick(BaseModel):
    # Used for inheritance
    ...


class ActionParameter(BaseModel):
    key: str
    value: str


class FormAction(BaseModel):
    actionMethodName: str
    parameters: Optional[List[ActionParameter]]


class ActionOnClick(OnClick):
    action: FormAction


class OpenLink(BaseModel):
    url: str


class OpenLinkOnClick(OnClick):
    openLink: OpenLink


class Button(BaseModel):
    # Used for Inheritance
    ...


class ImageButton(Button):
    name: str
    onClick: Optional[OnClick]
    icon: Optional[str]
    iconUrl: Optional[str]


class TextButton(Button):
    text: str
    onClick: Optional[OnClick]


class Widget(BaseModel):
    # Used for inheritance
    horizontalAlignment: Optional[str]
    ...


class ControlWidget(BaseModel):
    # Used for inheritance
    ...


class Icon(Widget):
    altText: Optional[str]
    imageType: str
    knownIcon: Optional[str]
    iconUrl: Optional[str]


class Color(BaseModel):
    ...

class ControlButton(ControlWidget):
    # Also recognized as a Button
    text: str
    icon: Optional[Icon]
    color: Optional[Color]
    onClick: Optional[OnClick]
    disabled: Optional[bool]
    altText: Optional[str]


class SwitchControl(ControlWidget):
    ...


class EndIcon(ControlWidget):
    ...


class _DecoratedText(BaseModel):
    icon: Optional[Icon]
    startIcon: Optional[Icon]
    topLabel: Optional[str]
    text: Optional[str]
    wrapText: Optional[bool]
    bottomLabel: Optional[str]
    onClick: Optional[OnClick]
    button: Optional[ControlButton]
    SwitchControl: Optional[SwitchControl]
    EndIcon: Optional[EndIcon]


class DecoratedText(Widget):
    decoratedText: _DecoratedText

    @classmethod
    def make(cls, **kwargs):
        return cls(
            decoratedText=_DecoratedText(**kwargs)
        )



class ButtonList(Widget):
    # https://developers.google.com/chat/api/reference/rest/v1/spaces.messages#buttonlist
    buttons: List[ControlButton]


class Action(BaseModel):
    # https://developers.google.com/chat/api/reference/rest/v1/spaces.messages#Action
    function: str
    parameters: Optional[ActionParameter]
    loadIndicator: Optional[str]
    persistValues: Optional[bool]


class SuggestionItem(BaseModel):
    # https://developers.google.com/chat/api/reference/rest/v1/spaces.messages#SuggestionItem
    text: str


class Suggestions(BaseModel):
    # https://developers.google.com/chat/api/reference/rest/v1/spaces.messages#suggestions
    suggestions: List[SuggestionItem]

class TextInputTypes:

    SINGLE_LINE = "SINGLE_LINE"
    MULTIPLE_LINE = "MULTIPLE_LINE"

class _TextInput(BaseModel):
    name: str
    label: str
    hintText: Optional[str]
    value: Optional[str]
    type: str
    onChangeAction: Optional[Action]
    initialSuggestions: Optional[Suggestions]
    autoCompleteAction: Optional[Action]


class TextInput(Widget):
    textInput: _TextInput

    @classmethod
    def make(cls, **kwargs):
        return cls(
            textInput=_TextInput(**kwargs)
        )


class SelectionType:

    CHECK_BOX = "CHECK_BOX"
    RADIO_BUTTON = "RADIO_BUTTON"
    SWITCH = "SWITCH"
    DROPDOWN = "DROPDOWN"

class SelectionItem(BaseModel):
    text: str
    value: str
    selected: Optional[bool] = False

class _SelectionInput(BaseModel):
    name: Optional[str]
    label: Optional[str]
    type: str
    items: List[SelectionItem]
    onChangeAction: Optional[Action]


class SelectionInput(Widget):
    selectionInput: _SelectionInput

    @classmethod
    def make(cls, **kwargs):
        return cls(
            selectionInput=_SelectionInput(**kwargs)
        )


class DateTimePickerType:

    DATE_AND_TIME = "DATE_AND_TIME"
    DATE_ONLY = "DATE_ONLY"
    TIME_ONLY = "TIME_ONLY"

class _DateTimePicker(BaseModel):
    name: str
    label: str
    type: str
    valueMsEpoch: Optional[int]
    timezoneOffsetDate: Optional[int]
    onChangeAction: Optional[Action]



class DateTimePicker(Widget):
    dateTimePicker: _DateTimePicker

    @classmethod
    def make(cls, **kwargs):
        return cls(
            dateTimePicker=_DateTimePicker(**kwargs)
        )

    @staticmethod
    def now():
        return int(time.time()*1000)


class Divider(Widget):
    ...

class Grid(Widget):
    ...


class TextParagraph(Widget):
    text: str


class Image(BaseModel):
    image: str
    onClick: Optional[OnClick]
    aspectRatio: Optional[float]
    altText: Optional[str]


class KeyValue(BaseModel):
    topLabel: str
    content: str
    contentMultiline: Optional[bool]
    bottomLabel: Optional[str]
    onClick: Optional[OnClick]
    icon: Optional[str]
    iconUrl: Optional[str]
    button: Optional[Button]


class WidgetMarkup(BaseModel):
    buttons: Optional[List[Button]]
    textParagraph: Optional[TextParagraph]
    image: Optional[Image]
    keyValue: Optional[KeyValue]


class Section(BaseModel):
    header: Optional[str]
    widgets: List[Union[Widget, WidgetMarkup]]


class CardAction(BaseModel):
    actionLabel: Optional[str]
    onClick: OnClick


class Card(ToDictMixin, BaseModel):
    header: Optional[CardHeader]
    sections: List[Section]
    cardActions: Optional[List[CardAction]]
    name: str


# https://developers.google.com/chat/api/reference/rest/v1/spaces.messages#switchcontrol
# https://developers.google.com/chat/api/reference/rest/v1/spaces.messages#actionresponse


class ActionStatus(BaseModel):
    statusCode: Optional[str]
    userFacingMessage: Optional[str]


class Dialog(BaseModel):
    body: Card


class DialogAction(BaseModel):
    actionStatus: Optional[ActionStatus]
    dialog: Optional[Dialog]


class ActionResponseTypes:
    TYPE_UNSPECIFIED = "TYPE_UNSPECIFIED"
    NEW_MESSAGE = "NEW_MESSAGE"
    UPDATE_MESSAGE = "UPDATE_MESSAGE"
    UPDATE_USER_MESSAGE_CARDS = "UPDATE_USER_MESSAGE_CARDS"
    REQUEST_CONFIG = "REQUEST_CONFIG"
    DIALOG = "DIALOG"

class ActionResponse(ToDictMixin, BaseModel):
    type: str
    url: Optional[str]
    dialogAction: Optional[DialogAction]

