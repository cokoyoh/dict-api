from typing import Union
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from kamusi import Trie
from models import Entry, WordResponse

app = FastAPI(
  title="Swahili language API",
  description="A simple dictionary API for the Swahili language",
  version="0.1.0",
  docs_url="/swagger",
  redoc_url="/redocs"
  )

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
@app.post("/words")
def create_word(entry: Entry):
  kamusi.insert(entry.word, entry.definitions)
  content = {"message": "word entry added successfully"}
  return JSONResponse(content=content, status_code=200)

@app.get("/words/{word}", response_model=WordResponse)
def get_word(word: str) -> WordResponse:
    entry = kamusi.search(word)
    if entry is None:
      raise HTTPException(status_code=404, detail={"message": f"{word} not found", "status": '404 Not found'})
    content = {"word": word, "definitions": entry.definitions}
    return JSONResponse(content, status_code=200)

@app.get('/autocomplete/')
def get_words_that_start_with_prefix(
  query: str = Query(..., min_length=2, description="The prefix to search")
):
  words = kamusi.autocomplete(query)
  content = {"prefix": query, "words": words}
  return JSONResponse(content, status_code=200)
