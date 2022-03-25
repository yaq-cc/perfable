# Left for implementing Messages

# https://developers.google.com/chat/api/reference/rest/v1/spaces.messages

import time
import json
from typing import Optional, List, Union, Literal, Type
from pydantic import BaseModel, validator
from enum import Enum
from .cards import Image
from .cards import CardHeader, CardAction

# Mixins
class ToDictMixin(BaseModel):

    def to_dict(self):
        return self.dict(exclude_none=True)


# Models
class Icon(BaseModel):
    altText: Optional[str]
    imageType: str
    knownIcon: Optional[str]
    iconUrl: Optional[str]


class ActionParameter(BaseModel):
    key: str
    value: str


class Action(BaseModel):
    # https://developers.google.com/chat/api/reference/rest/v1/spaces.messages#Action
    function: str
    parameters: Optional[List[ActionParameter]] = []
    loadIndicator: Optional[str]
    persistValues: Optional[bool]


class OpenLink(BaseModel):
    url: str
    openAs: Optional[str]
    onClose: Optional[str]


class OnClick(BaseModel):
    action: Optional[Action]
    openLink: Optional[OpenLink]
    openDynamicLinkAction: Optional[Action]
    # Has to be of Type Type due to python serial loading.
    card: Optional[Type]


class ImageCropStyle(BaseModel):
    # https://developers.google.com/chat/api/reference/rest/v1/spaces.messages#ImageCropType
    type: str
    aspectRatio: float


class Color(BaseModel):
    red: float
    green: float
    blue: float
    alpha: float


class BorderStyle(BaseModel):
    # https://developers.google.com/chat/api/reference/rest/v1/spaces.messages#BorderType
    type: str
    strokeColor: Optional[Color]
    cornerRadius: int

class ImageComponent(BaseModel):
    imageUri: str
    altText: Optional[str]
    cropStyle: Optional[ImageCropStyle]
    borderStyle: Optional[BorderStyle]


class TextParagraph(BaseModel):
    text: str


class ControlButton(BaseModel):
    # Also recognized as a Button
    text: str
    icon: Optional[Icon]
    color: Optional[Color]
    onClick: Optional[OnClick]
    disabled: Optional[bool]
    altText: Optional[str]


class SwitchControl(BaseModel):
    name: str
    value: str
    selected: Optional[bool] = False
    onChangeAction: Action
    # https://developers.google.com/chat/api/reference/rest/v1/spaces.messages#switchcontrol
    controlType: str


class DecoratedText(BaseModel):
    icon: Optional[Icon]
    startIcon: Optional[Icon]
    topLabel: Optional[str]
    text: Optional[str]
    wrapText: Optional[bool]
    bottomLabel: Optional[str]
    onClick: Optional[OnClick]
    button: Optional[ControlButton]
    SwitchControl: Optional[SwitchControl]
    EndIcon: Optional[Icon]


class TextInputTypes:

    SINGLE_LINE = "SINGLE_LINE"
    MULTIPLE_LINE = "MULTIPLE_LINE"


class SuggestionItem(BaseModel):
    # https://developers.google.com/chat/api/reference/rest/v1/spaces.messages#SuggestionItem
    text: str


class Suggestions(BaseModel):
    # https://developers.google.com/chat/api/reference/rest/v1/spaces.messages#suggestions
    suggestions: List[SuggestionItem]


class TextInput(BaseModel):
    name: str
    label: str
    hintText: Optional[str]
    value: Optional[str]
    type: str
    onChangeAction: Optional[Action]
    initialSuggestions: Optional[Suggestions]
    autoCompleteAction: Optional[Action]


class Button(BaseModel):
    text: str
    icon: Optional[Icon]
    color: Optional[Color]
    onClick: Optional[OnClick]
    disabled: bool = False
    altText: Optional[str]


class ButtonList(BaseModel):
    buttons: List[Button]


class SelectionType(str, Enum):

    CHECK_BOX = "CHECK_BOX"
    RADIO_BUTTON = "RADIO_BUTTON"
    SWITCH = "SWITCH"
    DROPDOWN = "DROPDOWN"


class SelectionItem(BaseModel):
    text: str
    value: str
    selected: Optional[bool] = False


class SelectionInput(BaseModel):
    name: Optional[str]
    label: Optional[str]
    type: str
    items: List[SelectionItem]
    onChangeAction: Optional[Action]


class DateTimePickerType(str, Enum):

    DATE_AND_TIME = "DATE_AND_TIME"
    DATE_ONLY = "DATE_ONLY"
    TIME_ONLY = "TIME_ONLY"


class DateTimePicker(BaseModel):
    name: str
    label: str
    type: str
    valueMsEpoch: Optional[int]
    timezoneOffsetDate: Optional[int]
    onChangeAction: Optional[Action]

    @staticmethod
    def now():
        return int(time.time()*1000)



class Divider(BaseModel):
    ...


class GridItem(BaseModel):
    id: str
    image: Optional[ImageComponent]
    title: str
    subtitle: Optional[str]
    textAlignment: Optional[str]
    # https://developers.google.com/chat/api/reference/rest/v1/spaces.messages#GridItemLayout 
    layout: Optional[str] 


class Grid(BaseModel):
    title: str
    items: List[GridItem]
    borderStyle: Optional[BorderStyle]
    columnCount: int
    onClick: OnClick


class Widget(BaseModel):
    horizontalAlignment: Optional[str]
    # Union field data
    textParagraph: Optional[TextParagraph]
    image: Optional[Image]
    decoratedText: Optional[DecoratedText]
    buttonList: Optional[ButtonList]
    textInput: Optional[TextInput]
    selectionInput: Optional[SelectionInput]
    dateTimePicker: Optional[DateTimePicker]
    divider: Optional[Divider]
    grid: Optional[Grid]


# The default "Card" requires a list of WidgetMarkup
class Section(BaseModel):
    header: Optional[str]
    widgets: List[Widget]


class Card(BaseModel):
    header: Optional[CardHeader]
    sections: List[Section]
    cardActions: Optional[List[CardAction]]
    name: Optional[str]


class Dialog(BaseModel):
    body: Card


# More here: https://developers.google.com/chat/api/reference/rest/v1/spaces.messages#Code
class ActionStatusCodes(str, Enum):
    OK = "OK"
    CANCELLED = "CANCELLED"
    UNKNOWN = "UNKNOWN"
    INVALID_ARGUMENT = "INVALID_ARGUMENT"
    DEADLINE_EXCEEDED = "DEADLINE_EXCEEDED"
    NOT_FOUND = "NOT_FOUND"
    ALREADY_EXISTS = "ALREADY_EXISTS"

class ActionStatus(BaseModel):
    statusCode: Optional[str]
    userFacingMessage: Optional[str]


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


class _ActionResponse(BaseModel):
    type: str
    url: Optional[str]
    dialogAction: Optional[DialogAction]

class ActionResponse(ToDictMixin, BaseModel):
    actionResponse: _ActionResponse

    @classmethod
    def make(cls, **kwargs):
        return cls(
            actionResponse=_ActionResponse(**kwargs)
        )
