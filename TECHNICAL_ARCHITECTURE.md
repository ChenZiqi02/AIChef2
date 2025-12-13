# AIChef Technical Architecture

## 1. Project Overview
**AIChef** is an intelligent recipe recommendation system that uses RAG (Retrieval-Augmented Generation) to turn simple ingredient lists into gourmet recipe suggestions. It features a "Fine Dining" aesthetic and a humorous, interactive AI consultant.

## 2. Tech Stack

### Frontend
- **Framework**: React 18 + Vite (TypeScript)
- **Styling**: Tailwind CSS v3 (Custom "Stone & Orange" Palette) + PostCSS
- **Icons**: Lucide React (Professional culinary icons)
- **State Management**: React Hooks (`useState`, `useEffect`) + SessionStorage Caching
- **Routing**: React Router DOM v6
- **HTTP Client**: Axios

### Backend
- **Framework**: FastAPI (Python 3.10+)
- **Server**: Uvicorn
- **API Style**: RESTful JSON API

### AI & Data
- **LLM**: Google Gemini 2.0 Flash (Strict Mode, High Intelligence)
  - **Safety**: `BLOCK_NONE` (Uncensored for creative flexibility)
  - **Strategy**: Direct Invocation (No Fallback, Patient Retry)
- **Vector Database**: ChromaDB (Persistent storage in `data/chroma_db_v3`)
- **Embeddings**: Sentence-Transformers (`paraphrase-multilingual-MiniLM-L12-v2`)
- **Orchestration**: LangChain (Google GenAI integration)

## 3. Key Features

### Intelligent Search (RAG)
1.  **Retrieval**: Searches 10k+ local recipes using vector similarity.
2.  **Rerank & Comment**: AI selects the best match and adds a humorous, personality-driven comment (e.g., roasting "weird" ingredients).
3.  **Strict Quality**: Configured to use `gemini-2.0-flash` exclusively for maximum reasoning capability.

### Interactive Consultant
- **Chat Interface**: Users can ask follow-up questions ("Can I make this spicy?", "I don't have an oven").
- **Context Awareness**: The AI knows the current recipe list and conversation history.

### Performance Optimization
- **Frontend Caching**: `sessionStorage` caches search results to ensure **instant (0ms)** page navigation when returning from details.
- **Efficient Vector Search**: Pre-computed embeddings for low-latency retrieval.

## 4. Project Structure

```
AIChef/
├── app/
│   ├── main.py            # FastAPI Entrypoint & Endpoints
│   ├── services.py        # Business Logic (Search, Chat)
│   └── models.py          # Pydantic Schemas
├── core/
│   ├── config.py          # Environment Configuration
│   ├── generator.py       # LLM Logic (Prompts, Safe Invoke)
│   ├── retriever.py       # ChromaDB Retrieval Interface
│   └── ingest.py          # Data Ingestion Scripts
├── data/
│   └── chroma_db_v3/      # Vector Database Files
├── frontend/
│   ├── src/
│   │   ├── Home.tsx       # Landing Page (Fine Dining Style)
│   │   ├── Results.tsx    # Search Results + AI Chat
│   │   ├── Detail.tsx     # Recipe rendering
│   │   └── App.tsx        # Routing & Layout
│   └── ...config files...
└── run.py                 # Unified Startup Script
```

## 5. Development Workflow
- **Backend**: `python run.py` (Port 8000)
- **Frontend**: `cd frontend && npm run dev` (Port 5173)
- **Env**: Requires `GEMINI_API_KEY` in `.env`.
