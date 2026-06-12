"""
src/llm/groq_client.py

Groq Client Wrapper

Model:
llama-3.3-70b-versatile

Features:
---------
1. Basic Completion
2. JSON Completion
3. Retry Handling
4. Health Check
5. Streamlit Compatible
6. Chunk Processing
"""

import json
import time
from typing import List, Dict, Any

from groq import Groq

from src.utils.config import (
    GROQ_API_KEY,
    GROQ_MODEL,
    GROQ_TEMPERATURE,
    GROQ_MAX_TOKENS
)

# =====================================================
# CLIENT
# =====================================================

_client = None


def get_client():
    """
    Lazy initialization of Groq Client
    """

    global _client

    if _client is None:

        if not GROQ_API_KEY:

            raise ValueError(
                "GROQ_API_KEY not configured.\n"
                "Add it to .streamlit/secrets.toml\n"
                "or environment variables."
            )

        _client = Groq(
            api_key=GROQ_API_KEY
        )

    return _client


# =====================================================
# BASIC COMPLETION
# =====================================================

def groq_completion(
    prompt: str,
    temperature: float = None,
    max_tokens: int = None
) -> str:

    temperature = (
        temperature
        if temperature is not None
        else GROQ_TEMPERATURE
    )

    max_tokens = (
        max_tokens
        if max_tokens is not None
        else GROQ_MAX_TOKENS
    )

    try:

        client = get_client()

        response = (
            client.chat.completions.create(

                model=GROQ_MODEL,

                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],

                temperature=temperature,

                max_tokens=max_tokens
            )
        )

        return (
            response
            .choices[0]
            .message.content
            .strip()
        )

    except Exception as e:

        print(
            f"GROQ Error: {e}"
        )

        return "{}"


# =====================================================
# RETRY COMPLETION
# =====================================================

def groq_completion_retry(
    prompt: str,
    retries: int = 3,
    wait_seconds: int = 2
) -> str:

    for attempt in range(retries):

        try:

            return groq_completion(
                prompt
            )

        except Exception as e:

            print(
                f"Attempt {attempt+1} failed: {e}"
            )

            time.sleep(
                wait_seconds
            )

    return "{}"


# =====================================================
# JSON COMPLETION
# =====================================================

def groq_json_completion(
    prompt: str
) -> Dict:

    try:

        response = groq_completion(
            prompt
        )

        start = response.find("{")
        end = response.rfind("}")

        if start >= 0 and end >= 0:

            json_text = response[
                start:end + 1
            ]

            return json.loads(
                json_text
            )

        return {}

    except Exception as e:

        print(
            f"JSON Parse Error: {e}"
        )

        return {}


# =====================================================
# SAFE JSON COMPLETION
# =====================================================

def groq_safe_json_completion(
    prompt: str
) -> Dict:

    try:

        response = groq_completion(
            prompt
        )

        response = response.strip()

        if response.startswith("```json"):

            response = (
                response
                .replace(
                    "```json",
                    ""
                )
                .replace(
                    "```",
                    ""
                )
            )

        return json.loads(
            response
        )

    except Exception:

        try:

            return groq_json_completion(
                prompt
            )

        except Exception:

            return {}


# =====================================================
# CHUNK PROCESSING
# =====================================================

def groq_chunk_completion(
    chunks: List[str],
    prompt_template: str
):

    outputs = []

    total = len(chunks)

    for idx, chunk in enumerate(
        chunks
    ):

        try:

            prompt = f"""
{prompt_template}

CONTENT:

{chunk}
"""

            response = groq_completion(
                prompt
            )

            outputs.append(
                response
            )

        except Exception as e:

            print(
                f"Chunk {idx+1}/{total} Error: {e}"
            )

    return outputs


# =====================================================
# MULTI CHUNK JSON
# =====================================================

def groq_chunk_json_completion(
    chunks: List[str],
    prompt_template: str
):

    outputs = []

    for chunk in chunks:

        try:

            prompt = f"""
{prompt_template}

CONTENT:

{chunk}
"""

            result = (
                groq_safe_json_completion(
                    prompt
                )
            )

            outputs.append(
                result
            )

        except Exception:

            pass

    return outputs


# =====================================================
# HEALTH CHECK
# =====================================================

def health_check():

    try:

        result = groq_completion(
            """
            Return ONLY:

            {"status":"ok"}
            """
        )

        return {

            "success": True,

            "response": result

        }

    except Exception as e:

        return {

            "success": False,

            "error": str(e)

        }


# =====================================================
# TEST CONNECTION
# =====================================================

def test_connection():

    try:

        result = groq_completion(
            "Return only word CONNECTED"
        )

        return {

            "success": True,

            "model": GROQ_MODEL,

            "response": result

        }

    except Exception as e:

        return {

            "success": False,

            "error": str(e)

        }


# =====================================================
# MODEL INFO
# =====================================================

def model_info():

    return {

        "provider": "Groq",

        "model": GROQ_MODEL,

        "temperature":
            GROQ_TEMPERATURE,

        "max_tokens":
            GROQ_MAX_TOKENS

    }


# =====================================================
# STREAMLIT STATUS
# =====================================================

def streamlit_status():

    try:

        result = health_check()

        if result["success"]:

            return "🟢 GROQ Connected"

        return "🔴 GROQ Failed"

    except Exception:

        return "🔴 GROQ Failed"


# =====================================================
# DEBUG
# =====================================================

if __name__ == "__main__":

    print("\nTesting GROQ\n")

    print(
        test_connection()
    )

    print()

    print(
        model_info()
    )

    print()

    print(
        health_check()
    )
  
