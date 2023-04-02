from pydantic import BaseModel


class BodyBible(BaseModel):
    date: str
    week_day: str
    title: str
    bible_name: str
    bible_range: str
    bible_text: list[dict[int, str]]

class BodyBibleContent(BaseModel):
    content_title: str
    content_data: list[dict[str, str]]

