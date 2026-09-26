"""Gemini-powered legal document generator."""

import os
import google.generativeai as genai
from dotenv import load_dotenv

from .prompts import SYSTEM_PROMPT, build_user_prompt

load_dotenv()

_GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
_GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash").strip()

if not _GEMINI_API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is not set. Add it to your .env file before running the backend."
    )

genai.configure(api_key=_GEMINI_API_KEY)


class GeminiDocumentGenerator:
    """Wraps the Gemini model for legal document generation."""

    def __init__(self, model_name: str = _GEMINI_MODEL):
        self.model_name = model_name
        self._model = genai.GenerativeModel(
            model_name=self.model_name,
            system_instruction=SYSTEM_PROMPT,
        )

    def generate_document(
        self,
        document_type: str,
        party_a: str,
        party_b: str,
        effective_date: str,
        jurisdiction: str,
        key_terms: str,
        additional_notes: str = "",
        temperature: float = 0.3,
        max_output_tokens: int = 4096,
    ) -> str:
        """Generate the legal document text via Gemini."""
        user_prompt = build_user_prompt(
            document_type=document_type,
            party_a=party_a,
            party_b=party_b,
            effective_date=effective_date,
            jurisdiction=jurisdiction,
            key_terms=key_terms,
            additional_notes=additional_notes,
        )

        generation_config = genai.types.GenerationConfig(
            temperature=temperature,
            max_output_tokens=max_output_tokens,
            top_p=0.95,
            top_k=40,
        )

        try:
            response = self._model.generate_content(
                user_prompt,
                generation_config=generation_config,
            )
        except Exception as exc:
            raise RuntimeError(f"Gemini generation failed: {exc}") from exc

        text = ""
        try:
            text = (response.text or "").strip()
        except Exception:
            # Fallback if response.text raises (e.g. safety block)
            if getattr(response, "candidates", None):
                parts = response.candidates[0].content.parts
                text = "\n".join(p.text for p in parts if getattr(p, "text", None))

        if not text:
            raise RuntimeError("Gemini returned an empty document.")

        # Strip stray code fences if the model adds them.
        if text.startswith("```"):
            text = text.strip("`")
            if text.lower().startswith("text"):
                text = text[4:]
        return text.strip()