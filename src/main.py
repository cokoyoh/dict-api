from typing import Union, List
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import JSONResponse
from kamusi import Trie
from models import Entry, WordResponse, AutocompleteResponse
from word_not_found_exception import WordNotFound

app = FastAPI(
    title="Swahili language API",
    description="A simple dictionary API for the Swahili language",
    version="0.1.0",
    docs_url="/swagger",
    redoc_url="/redocs",
)

kamusi = Trie()


@app.exception_handler(WordNotFound)
def word_not_found_handler(request: Request, exc: WordNotFound):
    return JSONResponse(
        status_code=404,
        content={"error": f"Word {exc.query} not found", "status": "404 Not found"},
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "Something went wrong...",
        },
    )


# Start of an amazing kamusi dictionary API
@app.get("/")
def home():
    return {"message": "hello world!"}


@app.get("/trie")
def dump_trie_dsa():
    return {"trie": kamusi}


@app.post("/words")
def create_word(entry: Entry):
    kamusi.insert(entry.word.lower(), entry.definitions)
    content = {"message": "word entry added successfully"}
    return JSONResponse(content=content, status_code=200)


@app.get("/search/", response_model=WordResponse)
def get_word(
    query: str = Query(..., min_length=3, description="The word to search")
) -> WordResponse:
    entry = kamusi.search(query.lower())
    if entry is None:
        raise WordNotFound(query)
    return JSONResponse(content=entry, status_code=200)


@app.get("/autocomplete/", response_model=AutocompleteResponse)
def get_words_that_start_with_prefix(
    query: str = Query(..., min_length=2, description="The prefix to autocomplete")
) -> AutocompleteResponse:
    words = kamusi.autocomplete(query.lower())
    content = {"prefix": query, "words": words}
    return JSONResponse(content, status_code=200)
