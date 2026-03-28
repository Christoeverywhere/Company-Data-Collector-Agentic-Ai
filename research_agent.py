import os
import json
from pydantic import ValidationError
from schema import CompanySchemaPartial
from prompts import build_research_prompt
from llm_clients import GeminiClient, GroqClient, CerebrasClient


class ResearchAgent:
    def __init__(self):
        self.clients = {
            "gemini": GeminiClient(),
            "groq": GroqClient(),
            "cerebras": CerebrasClient()
        }
        os.makedirs("outputs/raw", exist_ok=True)

    def _validate_output(self, source_name: str, data: dict) -> dict:
        try:
            validated = CompanySchemaPartial(**data)
            print(f"✅ {source_name} output validated successfully")
            return validated.model_dump(mode="json")
        except ValidationError as e:
            print(f"\n❌ Validation failed for {source_name}:")
            print(e)
            return {}

    def _save_output(self, source_name: str, company_name: str, data: dict):
        safe_name = company_name.lower().replace(" ", "_")
        path = f"outputs/raw/{safe_name}_{source_name}.json"

        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

        print(f"💾 Saved {source_name} output -> {path}")

    def _call_model(self, source_name: str, client, prompt: str, company_name: str) -> dict:
        try:
            print(f"\n🔍 Calling {source_name}...")
            raw_output = client.generate(prompt)
            validated_output = self._validate_output(source_name, raw_output)
            self._save_output(source_name, company_name, validated_output)
            return validated_output
        except Exception as e:
            print(f"❌ {source_name} failed: {e}")
            return {}

    def run(self, company_name: str) -> dict:
        prompt = build_research_prompt(company_name)

        results = {}
        for source_name, client in self.clients.items():
            results[source_name] = self._call_model(source_name, client, prompt, company_name)

        return results