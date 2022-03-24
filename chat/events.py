from typing import Optional, List, Union
from pydantic import BaseModel
from enum import Enum

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

