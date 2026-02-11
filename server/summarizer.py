import os
from typing import List
from openai import OpenAI
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from enum import Enum

# 1. SetUp
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
app    = FastAPI()

#2. Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Define the Data Model
class DocRequest(BaseModel):
    text: str

class Severity(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"

class RiskItem(BaseModel):
    description: str
    severity: Severity

class ComplianceReport(BaseModel):
    summary: str
    key_risks: List[RiskItem] # Changed from List[str] to List[RiskItem]
    obligations: List[str]
    recommended_actions: List[str]
    missing_info: str

# 4. The Logic
def summarize_with_reflection(text):
    print("Step 1: Drafting initial compliance summary...")

    # Pass 1: Initial Summary
    draft_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[ 
            {"role":"system", "content":"You are a strict FinTech Compliance Assistant. "
            "SCOPE GUARD: Only summarize documents related to financial regulations, KYC/AML, or legal compliance. "
            "If the input is general knowledge (like geography or history) or unrelated to compliance, "
            "do NOT answer the question. Instead, strictly state: 'OUT OF SCOPE: This content does not contain regulatory or compliance data.'"},
            {"role": "user", "content": text} 
        ],
        temperature=0.1,       # Keeps it factual
        max_tokens=300         # Keeps it concise
    )

    draft = draft_response.choices[0].message.content

    print("Step 2: Performing AI Reflection (Audit Pass)...")

    # Pass 2: The Reflection/Criticism
    # This is the 'Agentic' behavior where the AI checks its own work
    reflection_response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role":"system", "content": (
            "You are a Senior Compliance Auditor. Compare the DRAFT against the ORIGINAL text. "
            "Your job is to find 'hidden' multipliers that the draft missed. "
            "Specifically check for: "
            "1. Multipliers: Is the fine 'per account', 'per day', or 'per violation'? "
            "2. Deadlines: Are there specific timezones or 'business days' vs 'calendar days'? "
            "3. Conflict: Does this rule override a specific previous year's rule? "
            "If the draft missed any of these, state it clearly in your critique."
        )},
        {"role": "user", "content": f"ORIGINAL: {text}\n\nDRAFT: {draft}"}
        ],
        temperature=0.1,
        max_tokens=300 
    )

    critique = reflection_response.choices[0].message.content

    print("Step 3: Finalizing accurate report...")
    # Pass 3: Final Polished Output
    final_response = client.beta.chat.completions.parse(
        model="gpt-4o",
         messages=[
            {"role":"system", "content":
            "## ROLE\n"
            "You are a Senior Compliance Officer. Produce a high-precision structured report."
            
            "## PRECISION RULES (MANDATORY)\n"
            "- You MUST include specific dollar amounts and multipliers (e.g., 'per account', 'per day').\n"
            "- NEVER generalize these into 'hefty fines'. Use the exact numbers from the ORIGINAL text.\n"
            "- If the Critique identifies a missed multiplier, you MUST restore it from the ORIGINAL text.\n\n"
            
            "## SEVERITY SCoring\n"
            "For every item in 'Key Risks', assign a Severity level based on these criteria:\n"
            "- **CRITICAL**: Multipliers involved (per account, per day) or potential business shutdown.\n"
            "- **HIGH**: Large flat fines (>$10,000) or direct legal action/lawsuits.\n"
            "- **MEDIUM**: Operational changes required or minor flat fines.\n"
            "- **LOW**: Simple documentation updates or non-urgent notices.\n\n"
            
            "## FORMAT\n"
            "Output the final report in the requested JSON structure. "
            "Safety Disclaimer: This is an AI-generated summary for human review only."},
            {"role": "user", "content": f"""ORIGINAL TEXT: {text} DRAFT: {draft} CRITIQUE: {critique}"""} 
        ],
        response_format=ComplianceReport      
    )

    final = final_response.choices[0].message.parsed

    return {
        "draft": draft,
        "critique": critique,
        "final": final.model_dump() # Converting Pydantic object to dictionary
    }


@app.post("/summarize")
async def handle_summarize(request: DocRequest):
    try:
        if not request.text.strip():
            return {"error": "Input text cannot be empty"}, 400
        
        result = summarize_with_reflection(request.text)

        return {
            "draft": result["draft"],
            "critique": result["critique"],
            "final": result["final"]
        }
    except Exception as e:
        print(f"Server Error: {str(e)}")
        return {"error": "The AI Auditor is currently unavailable. Please check your API key or connection."}, 500