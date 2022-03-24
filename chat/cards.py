import json
from typing import Optional, List, Union, Literal
from pydantic import BaseModel, validator
from enum import Enum

# https://developers.google.com/chat/api/reference/rest/v1/cards


class ImageStyle(str, Enum):
    IMAGE = "IMAGE"
    AVATAR = "AVATAR"


class TextParagraph(BaseModel):
    text: str


class ActionParameter(BaseModel):
    key: str
    value: str


class FormAction(BaseModel):
    actionMethodName: str
    parameters: List[ActionParameter]


class OpenLink(BaseModel):
    url: str


class OnClick(BaseModel):
    action: Optional[FormAction]
    openLink: Optional[OpenLink]


class Image(BaseModel):
    imageUrl: str
    onClick: Optional[OnClick]
    aspectRatio: Optional[float]


class Icon(str, Enum):
    AIRPLANE = "AIRPLANE"
    BOOKMARK = "BOOKMARK"
    BUS = "BUS"
    CAR = "CAR"
    CLOCK = "CLOCK"
    CONFIRMATION_NUMBER_ICON = "CONFIRMATION_NUMBER_ICON"
    DOLLAR = "DOLLAR"
    DESCRIPTION = "DESCRIPTION"
    EMAIL = "EMAIL"
    # add more from here: https://developers.google.com/chat/api/reference/rest/v1/cards#icon


class TextButton(BaseModel):
    text: str
    onClick: Optional[OnClick]


class ImageButton(BaseModel):
    onClick: Optional[OnClick]
    name: Optional[str]
    # Union field icons
    icon: Optional[str]
    iconUrl: Optional[str]


class Button(BaseModel):
    textButton: Optional[TextButton]
    imageButton: Optional[ImageButton]


class KeyValue(BaseModel):
    topLabel: str
    content: str
    contentMultiline: bool = False
    bottomLabel: Optional[str]
    onClick: Optional[OnClick]
    # Union field icons
    icon: Optional[str]
    iconUrl: Optional[str]
    button: Optional[Button]


class WidgetMarkup(BaseModel):
    buttons: List[Button]
    # Union field "data"
    textParagraph: Optional[TextParagraph]
    image: Optional[Image]
    keyValue: Optional[KeyValue]


class CardAction(BaseModel):
    actionLabel: str
    onClick: OnClick


class Section(BaseModel):
    header: Optional[str]
    widgets: List[WidgetMarkup]


class CardHeader(BaseModel):
    title: str
    subtitle: Optional[str]
    imageStyle: str
    imageUrl: Optional[str]


class Card(BaseModel):
    header: CardHeader
    sections: List[Section]
    cardActions: Optional[List[CardAction]]
    name: Optional[str]


