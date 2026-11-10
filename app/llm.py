import os
import json
import requests

from dotenv import load_dotenv
from google import genai

load_dotenv()

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini")


# Streaming response
def stream_response(prompt, system_prompt, usage):

    if LLM_PROVIDER == "gemini":

        client = genai.Client(
            api_key=os.getenv("GEMINI_API_KEY")
        )

        response = client.models.generate_content_stream(
            model="gemini-3.5-flash-lite",
            contents=f"{system_prompt}\n\n{prompt}"
        )

        for chunk in response:
            if chunk.text:
                yield chunk.text

            if chunk.usage_metadata:
                usage["input_tokens"] = (
                    chunk.usage_metadata.prompt_token_count or 0
                )
                usage["output_tokens"] = (
                    chunk.usage_metadata.candidates_token_count or 0
                )

    elif LLM_PROVIDER == "ollama":

        response = requests.post(
            "http://localhost:11434/api/chat",
            json={
                "model": "qwen3.5:4b",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                "stream": True
            },
            stream=True,
            timeout=120
        )

        response.raise_for_status()

        for line in response.iter_lines():
            if line:
                data = json.loads(line)

                content = data.get("message", {}).get("content", "")

                if content:
                    yield content

                if data.get("done"):
                    usage["input_tokens"] = data.get(
                        "prompt_eval_count", 0
                    )
                    usage["output_tokens"] = data.get(
                        "eval_count", 0
                    )

    else:
        raise ValueError("Unsupported LLM provider")


# Generate conversation summary
def generate_summary(conversation):

    if LLM_PROVIDER == "gemini":

        client = genai.Client(
            api_key=os.getenv("GEMINI_API_KEY")
        )

        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=f"""
            Summarize this conversation.

            Return JSON with exactly these fields:
            title, summary, action_items.

            Conversation:
            {conversation}
            """,
            config={
                "response_mime_type": "application/json"
            }
        )

        return response.text

    elif LLM_PROVIDER == "ollama":

        response = requests.post(
            "http://localhost:11434/api/chat",
            json={
                "model": "qwen3.5:4b",
                "messages": [
                    {
                        "role": "system",
                        "content": "Return a valid JSON summary with title, summary and action_items."
                    },
                    {
                        "role": "user",
                        "content": conversation
                    }
                ],
                "format": "json",
                "stream": False
            },
            timeout=120
        )

        response.raise_for_status()

        return response.json()["message"]["content"]

    else:
        raise ValueError("Unsupported LLM provider")