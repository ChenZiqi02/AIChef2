# 🥦 AIChef - Fridge Rescue Assistant

> **"Don't know what to cook with your leftovers? Let AI Chef save the day!"**

![App Demo](image_21c592.jpg)

## 📖 Introduction

**AIChef** is an intelligent cooking assistant powered by **RAG (Retrieval-Augmented Generation)** technology. Unlike traditional recipe search engines, AIChef focuses on the **"Fridge Rescue"** scenario.

Users simply input the ingredients currently available in their fridge (e.g., *"I only have half an onion and two eggs"*). The system will:
1.  **Retrieve**: Search through a local vector database (ChromaDB) containing 10,000+ recipes to find the most relevant culinary inspirations.
2.  **Generate**: Use a Large Language Model (LLM) to act as a creative chef, teaching users how to adapt existing recipes to their limited ingredients—turning "leftovers" into delicious meals.

## ✨ Key Features

* **🥗 Smart Ingredient Matching**: Uses semantic search to understand ingredients (e.g., suggesting chicken if pork is missing).
* **💡 Adaptive Cooking Instructions**: The AI doesn't just copy-paste recipes; it intelligently modifies steps based on what you actually have.
* **⚡ Fast Local Retrieval**: Built on ChromaDB and BAAI Embeddings for millisecond-level response times.
* **💬 Interactive UI**: A clean, chat-based interface built with React, featuring streaming responses and recipe citations.
* **🔌 Flexible LLM Support**: Compatible with any OpenAI-style API (SiliconFlow Qwen, DeepSeek, Google Gemini, etc.).

## 🛠 Tech Stack

* **Frontend**: React, Node, HTML
* **Backend Logic**: Python, LangChain
* **Vector Database**: ChromaDB, FAISS
* **Embedding Model**: BAAI/bge-small-zh-v1.5 (HuggingFace)
* **LLM**: OpenAI-compatible APIs (SiliconFlow, DeepSeek, Google Gemini)

## 🚀 Quick Start

### 1. Prerequisites

Ensure you have Python 3.10+ installed.

```bash
### 2. Configuration

Create a `.env` file in the root directory:

```env
GEMINI_API_KEY=your_api_key_here
```

### 3. Startup (Two Terminals)

**Terminal 1: Start Backend**
```bash
python run.py
# Server starts at http://127.0.0.1:8000
```

**Terminal 2: Start Frontend**
```bash
cd frontend
npm install  # First time only
npm run dev
# App opens at http://127.0.0.1:5173
```

## 🎮 How to Use

1.  **Open the App**: Visit `http://127.0.0.1:5173` in your browser.
2.  **Home Page**: Admire the fine dining aesthetic. Enter ingredients (e.g., "Tomato, Egg") in the search bar or click a category icon.
3.  **Consultant**: Click "Consult". The AI will analyze your ingredients.
4.  **Results & Chat**: 
    - You will see a list of curated recipes.
    - **AI Consultant**: At the top, the AI (Gemini 2.0) will give a humorous, personalized recommendation.
    - **Interactive Chat**: Type in the chat box to ask follow-up questions (e.g., "I don't eat spicy food", "How do I prep the shrimp?").
5.  **View Details**: Click any recipe card to see step-by-step instructions.
6.  **My Collection**: Click the "Heart" icon on any recipe to save it to your favorites.

## 📝 Troubleshooting

- **429 Resource Exhausted**: The system will automatically retry or you can wait a moment. (We prioritize the smarter Gemini 2.0 model).
- **Blank Page**: Ensure you are running the frontend on `localhost` (127.0.0.1) to avoid CORS issues.

---
*Bon Appétit!* 👨‍🍳