import json
import logging
from typing import Any

from pydantic import BaseModel

from fastapi import FastAPI, APIRouter, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import HTMLResponse, StreamingResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from src.app.rag import (
    load_or_parse_data,
    initialize_chat_embeddings,
    initialize_index_engine,
    perform_rag_llama_search
)

app = FastAPI()

app.mount("/static", StaticFiles(directory="src/frontend/static"), name="static")

logger = logging.getLogger()
router = APIRouter()
templates = Jinja2Templates(directory="src/frontend")

engine = None

origins = [
    "http://localhost",
    "http://localhost:3100/",
    "http://localhost:3100/chat",
    "http://0.0.0.0:3100/",
    "http://0.0.0.0:3100/chat",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QuerySchema(BaseModel):
    message: str
    option: str


@router.on_event('startup')
async def initialize_llama() -> None:
    global engine
    documents = await load_or_parse_data()
    await initialize_chat_embeddings()
    engine = await initialize_index_engine(documents)

    logger.info("Serving the app...")
    print("Serving the app...")


@router.get("/hello", response_class=HTMLResponse)
async def hello() -> Any:
    print("Hello")
    return json.dumps({"answer": "Hello, World!"})


@router.get("/", response_class=HTMLResponse)
async def landing_page(request: Request) -> Any:
    return templates.TemplateResponse("index.html", context={"request": request, "title": "Chat App"})


@router.post("/chat")
async def chat_handler(query: QuerySchema) -> Any:
    query_term = query.message
    # rag_or_vector = query.option

    try:
        rag_response = await perform_rag_llama_search(
            engine=engine, query_term=query_term
        )
        print(rag_response)

        return json.dumps({"answer": str(rag_response)})

    except ValueError as e:
        logging.error(f"Error: {e}")
        return json.dumps({"answer": f"Error: {e}"}), 400


app.include_router(router)

