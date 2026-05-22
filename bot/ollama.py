import logging

import httpx

from bot.config import OLLAMA_MODEL, OLLAMA_URL_CHAT, TIMEOUT


async def process_prompt(prompt: str, system: str | None = None) -> str:
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    payload = {
        "model": OLLAMA_MODEL,
        "messages": messages,
        "stream": False,
    }
    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(TIMEOUT)) as client:
            logging.debug(f"DEBUG: Sending payload: {payload}")

            response = await client.post(
                OLLAMA_URL_CHAT, json=payload, headers={
                    "Content-Type": "application/json"}
            )
            response.raise_for_status()  # handle response error code
            data = response.json()

            logging.debug(f"DEBUG: Full response: {data}")
            return data.get("message", {}).get(
                "content", f"Unexpected format: {data.keys()}"
            )

    except httpx.HTTPStatusError as e:
        return f"Ollama API Error: {e.response.status_code} - {e.response.text}"
    except httpx.RequestError as e:
        logging.error("Connection error occurred", exc_info=True)
        return f"Connection Error: {repr(e)}"
    except KeyError:
        return "Error: Unexpected response format from Ollama"
    except Exception as e:
        return f"Unexpected Error: {repr(e)}"
