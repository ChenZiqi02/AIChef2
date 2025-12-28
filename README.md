# AIChef - Intelligent Recipe Assistant

AIChef is a Retrieval-Augmented Generation (RAG) system designed to transform basic ingredient lists into gourmet recipe recommendations. It combines a local vector database for accurate recipe retrieval with a Large Language Model (LLM) for personalized culinary advice.

## Project Overview

Unlike traditional recipe search engines that rely solely on keyword matching, AIChef employs a semantic search approach to understand the culinary context of user queries. The system features a "Fine Dining" aesthetic and includes an interactive AI Chef Consultant capable of adapting recipes to user preferences (e.g., dietary restrictions, flavor adjustments) in real-time.

## Key Features

### 1. Smart Retrieval & Deduplication
- **Vector Search**: utilizes ChromaDB for semantic retrieval from a dataset of over 10,000 recipes.
- **Auto-Deduplication**: Implements a similarity-based filtering mechanism (using `difflib`) to remove duplicate or highly similar recipe variants from search results.
- **Dynamic Candidate Expansion**: Automatically expands the search range (fetching 3x the requested limit) to ensure a full set of distinct recipes is returned after filtering.

### 2. Context-Aware Refinement
- **Interactive Chat**: Users can refine search results through natural language in the chat interface (e.g., "make it spicy", "I don't have an oven").
- **Automatic Query Optimization**: The backend uses an LLM to rewrite search queries based on user feedback, instantly refreshing the recipe list to match the new context.
- **Real-time Updates**: The frontend UI is tightly integrated with the backend search logic, allowing for seamless updates without page reloads.

### 3. AI Consultant
- **Personality**: The AI acts as a professional and humorous chef consultant.
- **Logic Validation**: Capable of identifying and playfully rejecting "dark cuisine" combinations (e.g., incompatible ingredients) while suggesting rational alternatives.
- **Reranking & Commentary**: The AI analyzes retrieved recipes to provide a summarized recommendation or specific advice on ingredient usage.

## Technical Architecture

### Tech Stack
- **Frontend**: React 18, Vite, TypeScript, Tailwind CSS
- **Backend**: FastAPI (Python), Uvicorn
- **AI/LLM**: Support for OpenAI-compatible APIs (SiliconFlow, DeepSeek), LangChain
- **Database**: ChromaDB (Vector Store)
- **Embeddings**: BAAI/bge-small-zh-v1.5 (Sentence Transformers)

### System Design
1.  **Ingestion**: Recipe data is processed and embedded into ChromaDB.
2.  **Query Processing**: User queries are analyzed and optionally rewritten by the LLM.
3.  **Retrieval**: The system performs a similarity search in the vector database.
4.  **Generation**: Retrieved documents are passed to the LLM to generate a contextual response or recommendation.
5.  **Performance**: Frontend caching mechanisms ensure instant navigation between search results and details.

## Quick Start

### Prerequisites
- Python 3.10+
- Node.js & npm

### Configuration
Create a `.env` file in the `AIChef/` directory with your API credentials:

```env
SILICONFLOW_API_KEY=your_api_key
SILICONFLOW_BASE_URL=https://api.siliconflow.cn/v1
SILICONFLOW_MODEL_NAME=deepseek-ai/DeepSeek-V3
```

### Running the Application

1. **Start Backend Server**
   ```bash
   python AIChef/run.py
   # Server listens on http://0.0.0.0:8000
   ```

2. **Start Frontend Client**
   ```bash
   cd AIChef/frontend
   npm install
   npm run dev
   # Application accessible at http://localhost:5173
   ```

## Development Reference
- **API Documentation**: Available at `http://127.0.0.1:8000/docs` when the backend is running.
- **Architecture**: See `TECHNICAL_ARCHITECTURE.md` (in Chinese) for a deep dive into the system design.