# Legal Document RAG Chat Prototype

⚠️ **Quick Experimental Prototype** - Simple RAG experiment with legal documents. Not for production use.

A basic proof-of-concept that lets you chat with legal documents using RAG (Retrieval-Augmented Generation). Built to experiment with LlamaIndex + Azure OpenAI on legal text.

## What it does

- Parses PDF legal documents (currently has a court opinion sample)
- Chunks and indexes the text using vector embeddings  
- Lets you ask questions about the document content
- Returns AI-generated responses based on the document

## Quick Start

1. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Set environment variables** (or just hardcode in `rag.py`)

   ```env
   AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=your_deployment
   AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT_NAME=your_embeddings
   ```

3. **Run it**

   ```bash
   uvicorn src.app.main:app --host=0.0.0.0 --port=3100
   ```

4. **Try it at** `http://localhost:3100`

## What's inside

- **FastAPI** - Simple web server
- **LlamaIndex** - Handles RAG pipeline (chunking, embeddings, retrieval)  
- **LlamaParse** - Extracts text from PDFs
- **Azure OpenAI** - LLM and embeddings (API keys hardcoded in `rag.py`)
- Basic HTML chat interface

## Experiment with it

- Ask questions about the legal document
- Try different document types in `src/data/`
- Modify chunk sizes, retrieval settings in the code
- Test different prompt approaches

## Limitations

- Hardcoded API keys (not secure)
- Basic error handling
- Single document focus
- No authentication
- Don't use responses for actual legal advice

Simple experiment, nothing fancy!
