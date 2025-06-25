import requests
import tempfile
import PyPDF2
import os
from config import LLM_PROVIDER, LLM_MODEL

def call_llm(prompt: str, provider: str, model: str) -> str:
    provider = provider.lower()
    if provider == "openai":
        try:
            import openai
            openai.api_key = os.getenv("OPENAI_API_KEY")
            response = openai.ChatCompletion.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=512,
                temperature=0.2,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"[OpenAI error: {e}]"
    elif provider == "anthropic":
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
            response = client.messages.create(
                model=model,
                max_tokens=512,
                temperature=0.2,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text.strip()
        except Exception as e:
            return f"[Anthropic error: {e}]"
    elif provider == "gemini":
        return "[Gemini support not implemented. Please use OpenAI or Anthropic for now.]"
    else:
        return f"[Unknown LLM provider: {provider}]"

def pdf_summarize(pdf_url: str):
    """Downloads PDF, extracts text, and summarizes using the configured LLM provider."""
    try:
        response = requests.get(pdf_url)
        response.raise_for_status()
        with tempfile.NamedTemporaryFile(delete=True, suffix=".pdf") as tmp:
            tmp.write(response.content)
            tmp.flush()
            reader = PyPDF2.PdfReader(tmp.name)
            text = "\n".join(page.extract_text() or "" for page in reader.pages)
            if not text.strip():
                return {"summary": "No extractable text found in PDF."}
            # Summarize using LLM
            summary = call_llm(f"Summarize this scientific paper:\n{text[:4000]}", LLM_PROVIDER, LLM_MODEL)
            return {"summary": summary}
    except Exception as e:
        return {"summary": f"Error processing PDF: {e}"} 