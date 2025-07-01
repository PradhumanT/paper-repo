"""
OpenAI structured output call utility for G-Eval detection.
"""

import logging
import time
from openai import OpenAI
from typing import Type
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    logging.error("OPENAI_API_KEY not set in environment")
    raise ValueError("OPENAI_API_KEY not set in environment")
client = OpenAI(api_key=api_key)

def call_openai_structured(
    prompt: str,
    schema: Type[BaseModel],
    field: str,
    model: str = "gpt-4o",
    max_retries: int = 5,
    temperature: float = 0.0
) -> int:
    """
    Return a 1–5 score using OpenAI structured output mode.
    """
    messages = [
        {"role": "system", "content": "You are a helpful evaluator."},
        {"role": "user", "content": prompt}
    ]
    for attempt in range(1, max_retries + 1):
        try:
            response = client.beta.chat.completions.parse(
                model=model,
                messages=messages,
                response_format=schema,
                temperature=temperature
            )
            score = getattr(response.choices[0].message.parsed, field)
            print(f"Response: {score} for prompt: {prompt}")
            return score
        except Exception as e:
            wait = 2 ** attempt
            logging.warning(
                f"Attempt {attempt}/{max_retries} failed: {e}. Retrying in {wait}s…"
            )
            time.sleep(wait)
    raise RuntimeError(f"OpenAI structured call failed after {max_retries} retries.") 