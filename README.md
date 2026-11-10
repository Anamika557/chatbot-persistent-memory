# AI Chatbot with Persistent Memory

An AI-powered chatbot built using Python, Streamlit, PostgreSQL, and LLM integration. It stores conversations so users can revisit and continue previous chats.

## Features

- AI chatbot with streaming responses.
- Supports Google Gemini and Ollama.
- Persistent chat history using PostgreSQL.
- Create and resume multiple chat sessions.
- Customizable system prompts.
- Automatic chat titles.
- Conversation summarization with structured JSON.
- Pydantic validation.
- Token usage tracking.
- Secure environment variable configuration using `.env`.

## Technologies Used

- Python
- Streamlit
- PostgreSQL
- SQLAlchemy
- Google Gemini API
- Ollama (Qwen 3.5:4B)
- Pydantic

## Project Structure

```text
chatbot-persistent-memory/
│
├── app/
│   ├── chat.py
│   ├── database.py
│   ├── llm.py
│   ├── main.py
│   ├── models.py
│   └── schemas.py
│
├── streamlit_app.py
├── requirements.txt
├── .gitignore
└── .env
```

## Setup Instructions

1. Clone the repository.
2. Create and activate a Python virtual environment.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file and configure:

```env
DB_PASSWORD=your_postgresql_password
LLM_PROVIDER=gemini
GEMINI_API_KEY=your_gemini_api_key
```

5. Create a PostgreSQL database named `chatbot_memory_db`.
6. Start the application:

```bash
streamlit run streamlit_app.py
```

## Model Switching

Set `LLM_PROVIDER` in `.env`:

- `gemini` – Google Gemini API
- `ollama` – Local Ollama model

## Security

API keys and database credentials are stored in `.env` and should never be committed to GitHub.
