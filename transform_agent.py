import os
import json
import requests
from pydantic import ValidationError
from schema import CompanySchemaPartial
from transform_prompts import build_transform_prompt
from llm_clients import extract_json
from config import GROQ_API_KEY


class TransformAgent:
    def __init__(self):
        self.api_key = GROQ_API_KEY
        self.url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = "llama-3.3-70b-versatile"
        os.makedirs("outputs/final", exist_ok=True)

    def _call_transform_llm(self, prompt: str) -> dict:
        if not self.api_key:
            raise ValueError("GROQ_API_KEY is missing for TransformAgent")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are a structured JSON consolidation agent. "
                        "Return ONLY valid JSON. No markdown. No explanations."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.1,
            "max_tokens": 4096
        }

        response = requests.post(self.url, headers=headers, json=payload, timeout=90)
        response.raise_for_status()
        data = response.json()

        text = data["choices"][0]["message"]["content"]
        print(f"✅ TransformAgent used model: {self.model}")
        return extract_json(text)

    def run(self, company_name: str, research_outputs: dict) -> dict:
        valid_outputs = {k: v for k, v in research_outputs.items() if v}

        if not valid_outputs:
            print("❌ No valid Agent 1 outputs available for transformation")
            return {}

        prompt = build_transform_prompt(company_name, valid_outputs)

        try:
            transformed = self._call_transform_llm(prompt)

            validated = CompanySchemaPartial(**transformed)
            final_output = validated.model_dump(mode="json")

            print("✅ Agent 2 transformed output validated successfully")

        except ValidationError as e:
            print("\n❌ Agent 2 transformed output validation failed:")
            print(e)
            return {}

        except Exception as e:
            print(f"❌ TransformAgent failed: {e}")
            return {}

        safe_name = company_name.lower().replace(" ", "_")
        path = f"outputs/final/{safe_name}_final.json"

        with open(path, "w", encoding="utf-8") as f:
            json.dump(final_output, f, indent=4)

        print(f"💾 Saved final transformed output -> {path}")
        return final_output