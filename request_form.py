from pydantic import BaseModel


class LabeledData(BaseModel):
    check1: bool
    check2: bool
    check3: bool
    id: int
    text: str
    labeledText: str
    nickName: str

class CheckedData(BaseModel):
    label: int
    nick_name: str
    target: str
    text: str
    id: int