from pydantic import BaseModel


class Message(BaseModel):
    message: str

class Channel(BaseModel):
    id: int

class Transmission(BaseModel):
    id_channel: int
    message: str