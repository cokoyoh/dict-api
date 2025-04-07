from typing import Union
from fastapi import FastAPI
from kamusi import Trie
from models import Entry

app = FastAPI()
kamusi = Trie()


@app.get("/")
def read_root():
    return {"message": "hello world!"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/users/{user_id}")
def get_user(user_id: int):
  return {"user_id": user_id}

@app.get("/users")
def list_users(active: bool = True, sort: str = "name"):
  return {"active": active, "sort": sort}

@app.get("/users/{user_id}/posts")
def get_user_posts(user_id: int, limit: int = 10, sort: str = 'desc'):
  return {
    "user_id": user_id,
    "limit": limit,
    "sort": sort
  }

# Start of an amazing kamusi dictionary
@app.post('/words')
def create_word(entry: Entry):
  kamusi.insert(entry.word, entry.definitions)
  neno = kamusi.search(entry.word)
  return {"word": entry.word, "definitions": neno.definitions}
