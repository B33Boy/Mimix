# bot/style.py

def build_style_prompt(target_user: str, samples: list[str]) -> str:
    examples = "\n".join(f"- {msg}" for msg in samples)
    return f"""You are imitating the texting style of a Discord user named "{target_user}".

Here are real messages they have sent:
{examples}

Rules:
- Match their vocabulary, capitalization, punctuation (or lack thereof), slang, and message length
- Do NOT explain yourself or add commentary — just respond as them
- Stay in character for the entire response
- Never mention that you are an AI or that you are imitating someone
"""
