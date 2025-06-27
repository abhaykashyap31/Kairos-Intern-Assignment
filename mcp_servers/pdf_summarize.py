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
            client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=512,
                temperature=0.2,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"[OpenAI error: {e}]"
    elif provider == "gemini":
        try:
            import google.generativeai as genai
        except ImportError:
            raise ImportError("google-generativeai is not installed. Please install it with 'pip install google-generativeai'.")
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            return "[Gemini error: GOOGLE_API_KEY environment variable not set.]"
        try:
                genai.configure(api_key=api_key)
                model_obj = genai.GenerativeModel(model)
                response = model_obj.generate_content(prompt, stream=True)

                # Stream and accumulate the response
                output = ""
                for chunk in response:
                    if chunk.text:
                        print(chunk.text, end="", flush=True)  # Real-time console output
                        output += chunk.text

                return output.strip()
        except Exception as e:
            return f"[Gemini error: {e}]"
    elif provider == "anthropic":
        try:
            import anthropic
        except ImportError:
            raise ImportError("anthropic is not installed. Please install it with 'pip install anthropic'.")
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            return "[Anthropic error: ANTHROPIC_API_KEY environment variable not set.]"
        try:
            client = anthropic.Anthropic(api_key=api_key)
            response = client.messages.create(
                model=model,
                max_tokens=512,
                temperature=0.2,
                messages=[{"role": "user", "content": prompt}]
            )
            # Claude v3 returns content as a list of content blocks
            if hasattr(response, 'content') and isinstance(response.content, list):
                return " ".join([c.text for c in response.content if hasattr(c, 'text')])
            return str(response)
        except Exception as e:
            return f"[Anthropic error: {e}]"
    else:
        return f"[Unknown or unsupported LLM provider: {provider}]"

def pdf_summarize(pdf_url: str):
    """Downloads PDF, extracts text, and summarizes using the configured LLM provider."""
    try:
        # Auto-convert arXiv abs links to PDF links
        if "arxiv.org/abs/" in pdf_url:
            pdf_url = pdf_url.replace("/abs/", "/pdf/")
            if not pdf_url.endswith(".pdf"):
                pdf_url += ".pdf"
        response = requests.get(pdf_url)
        response.raise_for_status()
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(response.content)
            tmp_path = tmp.name
        try:
            reader = PyPDF2.PdfReader(tmp_path)
            text = "\n".join(page.extract_text() or "" for page in reader.pages)
            if not text.strip():
                return {"summary": "No extractable text found in PDF."}
            # Summarize using LLM with a detailed, technical prompt
            prompt = (
                "Capture all important technical terms, mathematical formulations, and key results to summarize this scientific paper in extreme detail. "
                "Do not oversimplify and keep summary as long as possible. Use technical language and include equations or definitions if present.\n"
                f"{text[:4000]}"
            )
            summary = call_llm(prompt, LLM_PROVIDER, LLM_MODEL)
            return {"summary": summary}
        finally:
            os.remove(tmp_path)
    except Exception as e:
        return {"summary": f"Error processing PDF: {e}"} 