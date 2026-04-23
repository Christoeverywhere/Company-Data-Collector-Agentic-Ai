# Radix Multi-Agent Workflow

A modular **multi-agent AI workflow system** built in Python that converts natural language user prompts into structured UI definitions and generated code (Python/React), with validation and transformation stages for safer, more reliable output.

## Overview

This project implements a **Radix-style multi-agent workflow** where different agents handle specialized tasks in sequence:

- **Research Agent** → Understands the user prompt and extracts intent, fields, and UI requirements
- **Transform Agent** → Converts the structured interpretation into schema / UI definition / code-ready format
- **Validation Gate** → Verifies correctness, completeness, and reduces hallucinations before final output

The system is designed to make **UI + code generation more structured, modular, and reliable** compared to a single-step LLM call.

---

## Features

- Multi-agent workflow architecture
- Prompt-to-structured-UI conversion
- Python / React code generation pipeline
- Validation gate to reduce incorrect outputs
- Centralized prompt templates
- Configurable LLM clients
- Schema-based intermediate representations
- Test-ready project structure
- Output storage support

---

## Project Structure

```bash
radix-multi-agent-workflow/
│
├── main.py                  # Entry point to run the full multi-agent workflow
├── config.py                # Configuration settings (models, flags, environment values)
├── llm_clients.py           # LLM client wrappers / API integrations
├── prompts.py               # Core prompts used across the workflow
├── schema.py                # Pydantic/data schemas for structured outputs
├── research_agent.py        # Agent responsible for understanding the prompt and extracting intent
├── transform_agent.py       # Agent that converts research output into structured UI/code-ready output
├── transform_prompts.py     # Prompt templates specific to transformation logic
├── validation_gate.py       # Final validation layer to check correctness and reduce hallucinations
│
├── tests/                   # Unit/integration tests
├── outputs/                 # Generated outputs / saved workflow results
├── pytest.ini               # Pytest configuration
└── .gitattributes           # Git settings
