import ollama
import re


def clean_response(text):

    text = re.sub(
        r"```.*?```",
        "",
        text,
        flags=re.DOTALL
    )

    text = re.sub(
        r'[\"“”]',
        "",
        text
    )

    return text.strip()


def ask_coding_ai(prompt, mode="english"):

    if mode == "hinglish":

        system_prompt = """
You are ROBIN coding assistant.

STRICT RULES:
- Reply ONLY in Hinglish
- Hindi in English letters only
- MAX 1 sentence
- Under 20 words
- Beginner friendly
- No paragraphs

Example:
Python ek programming language hai jo coding easy banati hai.
"""

    else:

        system_prompt = """
You are ROBIN coding assistant.

STRICT RULES:
- Reply ONLY in English
- MAX 1 sentence
- Under 20 words
- Beginner friendly
- No paragraphs
- No examples unless asked

Example:
Python is a programming language used for coding.
"""

    try:

        response = ollama.chat(
            model="qwen2.5:3b",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        reply = response[
            "message"
        ][
            "content"
        ].strip()

        print(
            "💻 Coding raw:",
            reply
        )

        return clean_response(
            reply
        )

    except Exception as e:

        print(
            "❌ Coding error:",
            e
        )

        return (
            "Sorry, coding failed."
        )


if __name__ == "__main__":

    print(
        ask_coding_ai(
            "what is python"
        )
    )