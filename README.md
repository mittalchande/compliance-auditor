Compliance Auditor: AI-Powered 3-Pass Reflection Pipeline

![Compliance Auditor Dashboard](./app-demo.jpg)

A high-precision FinTech tool designed to extract regulatory obligations and risk multipliers from dense legal documents. Unlike standard summarizers, this tool uses an Agentic Reflection Architecture to ensure no financial penalties (like "per account" or "per day" fines) are missed.

🚀 The Problem
Standard LLMs often "hallucinate" or generalize dense legal text, losing critical "hidden multipliers" during summarization (e.g., turning a "$25k per account" fine into a "heavy fine").

🧠 The Solution: 3-Pass Reflection Logic
This project implements a three-stage cognitive pipeline:

Pass 1: Extraction (GPT-4o-mini) - Rapidly drafts initial compliance points with a "Scope Guard" to reject non-regulatory content.

Pass 2: Audit (GPT-4o) - A "Senior Auditor" agent compares the draft against the original source to find missed multipliers, deadlines, or rule overrides.

Pass 3: Synthesis (GPT-4o + Structured Outputs) - Combines the draft and critique into a final, high-precision JSON report with automated Severity Scoring (Critical, High, Medium, Low).

🛠️ Tech Stack
Frontend: React, TypeScript, CSS3 (Animations & Flexbox)

Backend: FastAPI, Python, Pydantic (Structured Data Validation)

AI: OpenAI GPT-4o API, Beta Chat Completions Parse (for strict JSON schema adherence)

Tools: Axios, Dotenv

✨ Key Features
Agentic Critique: The AI self-corrects before showing the user the final result.

Severity Pulse: Visual "Critical" alerts for high-impact financial risks using CSS keyframes.

Domain Guardrails: Rejects general knowledge queries (e.g., "What is the capital of France?") to maintain professional utility and persona integrity.

Safety Disclaimer: Built-in transparency regarding missing information to ensure a "Human-in-the-Loop" workflow.
