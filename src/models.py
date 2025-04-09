from typing import List, Optional
from pydantic import BaseModel


class Entry(BaseModel):
    word: str
    # is_end_of_word: Optional[bool]
    definitions: Optional[List[str]]


class WordResponse(BaseModel):
    word: str
    definitions: List[str]


class AutocompleteResponse(BaseModel):
    prefix: str
    words: List[WordResponse]
