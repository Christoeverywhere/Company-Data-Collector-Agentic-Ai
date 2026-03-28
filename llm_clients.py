import json
import re
import time
import requests
from config import GEMINI_API_KEY, GROQ_API_KEY, CEREBRAS_API_KEY


def extract_json(response_content) -> dict:
    if isinstance(response_content, list):
        parts = []
        for item in response_content:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict):
                if "text" in item:
                    parts.append(str(item["text"]))
                else:
                    parts.append(str(item))
        text = "".join(parts)
    else:
        text = str(response_content)

    text = text.strip()
    text = text.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    match = re.search(r"\{.*", text, re.DOTALL)
    if match:
        candidate = match.group(0).strip()

        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            pass

        fixed = candidate

        open_braces = fixed.count("{")
        close_braces = fixed.count("}")
        if open_braces > close_braces:
            fixed += "}" * (open_braces - close_braces)

        open_brackets = fixed.count("[")
        close_brackets = fixed.count("]")
        if open_brackets > close_brackets:
            fixed += "]" * (open_brackets - close_brackets)

        try:
            return json.loads(fixed)
        except json.JSONDecodeError:
            pass

    raise ValueError(f"Could not extract valid JSON from model response:\n{text[:1000]}")


class GeminiClient:
    def __init__(self):
        self.api_key = GEMINI_API_KEY
        self.models = [
            "gemini-2.5-flash",
            "gemini-1.5-flash"
        ]

    def generate(self, prompt: str) -> dict:
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is missing")

        last_error = None

        for model in self.models:
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={self.api_key}"

                payload = {
                    "contents": [
                        {
                            "parts": [
                                {"text": prompt}
                            ]
                        }
                    ],
                    "generationConfig": {
                        "temperature": 0.1,
                        "maxOutputTokens": 4096
                    }
                }

                response = requests.post(url, json=payload, timeout=60)
                response.raise_for_status()
                data = response.json()

                parts = data["candidates"][0]["content"]["parts"]
                print(f"✅ Gemini used model: {model}")
                return extract_json(parts)

            except Exception as e:
                print(f"⚠️ Gemini model failed: {model} -> {e}")
                last_error = e
                time.sleep(1)

        raise ValueError(f"All Gemini models failed. Last error: {last_error}")


class GroqClient:
    def __init__(self):
        self.api_key = GROQ_API_KEY
        self.url = "https://api.groq.com/openai/v1/chat/completions"
        self.models = [
            "llama-3.3-70b-versatile",
            "llama-3.1-8b-instant"
        ]

    def generate(self, prompt: str) -> dict:
        if not self.api_key:
            raise ValueError("GROQ_API_KEY is missing")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        last_error = None

        for model in self.models:
            try:
                payload = {
                    "model": model,
                    "messages": [
                        {
                            "role": "system",
                            "content": (
                                "You are a structured data extraction assistant. "
                                "Return ONLY valid JSON. No markdown. No explanations. "
                                "All enum values must strictly follow the user prompt."
                            )
                        },
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.1,
                    "max_tokens": 4096
                }

                response = requests.post(self.url, headers=headers, json=payload, timeout=60)
                response.raise_for_status()
                data = response.json()

                text = data["choices"][0]["message"]["content"]
                print(f"✅ Groq used model: {model}")
                return extract_json(text)

            except Exception as e:
                print(f"⚠️ Groq model failed: {model} -> {e}")
                last_error = e
                time.sleep(1)

        raise ValueError(f"All Groq models failed. Last error: {last_error}")


class CerebrasClient:
    def __init__(self):
        self.api_key = CEREBRAS_API_KEY
        self.url = "https://api.cerebras.ai/v1/chat/completions"
        self.models = [
            "llama3.1-8b",
            "llama-3.3-70b"
        ]

    def generate(self, prompt: str) -> dict:
        if not self.api_key:
            raise ValueError("CEREBRAS_API_KEY is missing")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        last_error = None

        for model in self.models:
            try:
                payload = {
                    "model": model,
                    "messages": [
                        {
                            "role": "system",
                            "content": (
                                "You are a structured data extraction assistant. "
                                "Return ONLY valid JSON. No markdown. No explanations. "
                                "All enum values must strictly follow the user prompt."
                            )
                        },
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.1,
                    "max_completion_tokens": 4096,
                    "top_p": 1
                }

                response = requests.post(self.url, headers=headers, json=payload, timeout=60)
                response.raise_for_status()
                data = response.json()

                text = data["choices"][0]["message"]["content"]
                print(f"✅ Cerebras used model: {model}")
                return extract_json(text)

            except Exception as e:
                print(f"⚠️ Cerebras model failed: {model} -> {e}")
                last_error = e
                time.sleep(1)

        raise ValueError(f"All Cerebras models failed. Last error: {last_error}")