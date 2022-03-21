from typing import Optional, List
from pydantic import BaseModel


class Widget(BaseModel):
    ...

class TextWidget(Widget):

    class _TextWidget(BaseModel):
        text: str
    
    textWidget: _TextWidget

    @classmethod
    def make(cls, **kwargs):
        return cls(
            textWidget = cls._TextWidget(**kwargs)
        )


# text = TextWidget(textWidget=TextWidget._TextWidget(text="hi!~"))
text = TextWidget.make(text="Hello World!")
print(text.dict())


# class Widget(BaseModel):
#     ...

# class _TextWidget(BaseModel):
#     text: str

# class TextWidget(Widget):
#     textWidget: _TextWidget

# class _ImageWidget(BaseModel):
#     image: str

# class ImageWidget(Widget):
#     imageWidget: _ImageWidget

# class Widgets(BaseModel):
#     widgets: List[Widget]

# text = TextWidget(textWidget=_TextWidget(text="Hi"))
# image = ImageWidget(imageWidget=_ImageWidget(image="some.url/path/img.png"))

# widgets = Widgets(widgets=[text, image])

# print(widgets.dict())