import os
from pathlib import Path

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai

# Load .env from the project root folder
ENV_FILE = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(ENV_FILE)

router = APIRouter()


class DocumentRequest(BaseModel):
    document_type: str
    party_one: str
    party_two: str
    terms: str
    effective_date: str


@router.post("/generate")
def generate_document(data: DocumentRequest):
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="GEMINI_API_KEY is missing. Check the .env file."
        )

    prompt = f"""
You are a legal document drafting assistant.

Create a clear, well-organized legal document draft
for educational purposes using the details below.

Document type: {data.document_type}
First party: {data.party_one}
Second party: {data.party_two}
Effective date: {data.effective_date}

Terms and conditions:
{data.terms}

Include:
1. Document title
2. Details of both parties
3. Terms and conditions
4. Effective date
5. Signature sections

Use clear, professional language.
Do not invent missing personal or legal details.
Include a note that a qualified lawyer should review
the document before official use.
"""

    try:
        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt
        )

        if not response.text:
            raise HTTPException(
                status_code=500,
                detail="The AI returned an empty document. Please try again."
            )

        return {"document": response.text}

    except HTTPException:
        raise

    except Exception as error:
        error_message = str(error)

        if "503" in error_message or "UNAVAILABLE" in error_message:
            raise HTTPException(
                status_code=503,
                detail="Gemini AI is temporarily busy. Please try again."
            )

        raise HTTPException(
            status_code=500,
            detail=f"Document generation failed: {error_message}"
        )
