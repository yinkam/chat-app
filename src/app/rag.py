from llama_index.core.base.base_query_engine import BaseQueryEngine
from llama_parse import LlamaParse
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, Settings, Response
from llama_index.core.chat_engine.types import BaseChatEngine, AgentChatResponse
from llama_index.core.schema import Document

from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.legacy.embeddings.azure_openai import AzureOpenAIEmbedding

import os
import pickle
import nest_asyncio

from typing import Sequence
from dotenv import load_dotenv

# nest_asyncio.apply()

load_dotenv()

llamaparse_api_key = "llx-5bfaUGBLUcMfFr4B4UkDiuee6qQg4hrEOcmA4wU900gbYiAa"


async def load_or_parse_data():
    data_file = "./src/data/parsed_data.pkl"

    if os.path.exists(data_file):
        with open(data_file, "rb") as f:
            parsed_data = pickle.load(f)
    else:
        # Perform the parsing step and store the result in llama_parse_documents
        # llama_parse_documents = LlamaParse(api_key=llamaparse_api_key, result_type="markdown").load_data("./data/uber_10q_march_2022.pdf")
        # llama_parse_documents = LlamaParse(api_key=llamaparse_api_key, result_type="markdown").load_data("./data/presentation.pptx")
        # llama_parse_documents = LlamaParse(api_key=llamaparse_api_key, result_type="markdown").load_data(
        #     ["./data/presentation.pptx", "./data/uber_10q_march_2022.pdf"])

        parser = LlamaParse(api_key=llamaparse_api_key, result_type="text")
        parse_documents = SimpleDirectoryReader(input_dir="./src/data/",
                                                file_extractor={".pdf": parser}).load_data()

        # Save the parsed data to a file
        with open(data_file, "wb") as f:
            pickle.dump(parse_documents, f)

        # Set the parsed data to the variable
        parsed_data = parse_documents

    return parsed_data


# Call the function to either load or parse the data

async def initialize_chat_embeddings() -> None:

    azure_endpoint = "https://ragmongodbcoretest.openai.azure.com/"
    api_key = "34103bff494d4d63b7af3b5d250613a3"
    api_version = "2024-02-01"

    chat_deployment_name = os.environ.get("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME")
    embeddings_deployment_name = os.environ.get("AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT_NAME")

    llm = AzureOpenAI(
        deployment_name=chat_deployment_name,
        azure_endpoint=azure_endpoint,
        api_key=api_key,
        api_version=api_version,
    )

    embed_model = AzureOpenAIEmbedding(
        model="text-embedding-ada-002",
        deployment_name=embeddings_deployment_name,
        api_key=api_key,
        azure_endpoint=azure_endpoint,
        api_version=api_version,
    )

    Settings.llm = llm
    Settings.embed_model = embed_model


async def initialize_index_engine(documents: Sequence[Document]) -> BaseQueryEngine:
    index = VectorStoreIndex.from_documents(documents)
    engine = index.as_query_engine()
    
    return engine


async def perform_rag_llama_search(engine: BaseQueryEngine | None, query_term: str) -> Response:

    try:
        return engine.query(query_term)

    except Exception:
        return Response(response="The requested data is not Found.")


