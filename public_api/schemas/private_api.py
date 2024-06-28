from pydantic import BaseModel


class UploadFileResponse(BaseModel):
    filename: str


class FileURLResponse(BaseModel):
    filename: str
    life_time: int
    url: str
