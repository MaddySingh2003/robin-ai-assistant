import ollama
import re


# =====================================
# MEMORY
# =====================================

conversation_history = [
    {
        "role": "system",
        "content": """
You are ROBIN, a smart female AI assistant.

RULES:

1. Keep answers SHORT.
2. Talk naturally like Siri/Jarvis.
3. Be smart and friendly.
4. Never give long essays unless asked.

LANGUAGE RULES:

ENGLISH MODE:
- Reply ONLY in English.

HINDI MODE:
- Reply ONLY in Hindi script.
Example:
"मशीन लर्निंग एक तकनीक है"

HINGLISH MODE:
VERY IMPORTANT:
- Use ONLY Hindi written in English letters.
- NEVER use Hindi script.
- NEVER write Devanagari letters.
- Speak naturally like Indians chat.

GOOD Hinglish:
"Machine learning ek technique hai jo computer ko data se seekhne me help karti hai."

BAD Hinglish:
"मशीन लर्निंग एक तकनीक है"

BAD Hinglish:
"Machine learning is a technology"

Always follow requested language strictly.
"""
    }
]

# =====================================
# LANGUAGE DETECTION
# =====================================

def detect_language_mode(text):

    text = text.lower()

    # Hinglish FIRST (highest priority)

    hinglish_keywords = [
        "hinglish",
        "in hinglish",
        "hinglish me",
        "hinglish mein",
        "explain in hinglish"
    ]

    if any(word in text for word in hinglish_keywords):
        return "hinglish"

    # Hindi

    hindi_keywords = [
        "in hindi",
        "hindi me",
        "hindi mein",
        "explain in hindi"
    ]

    if any(word in text for word in hindi_keywords):
        return "hindi"

    # English

    english_keywords = [
        "in english",
        "english me",
        "explain in english"
    ]

    if any(word in text for word in english_keywords):
        return "english"

    return "auto"


# =====================================
# ASK AI
# =====================================

def ask_api(prompt):

    mode = detect_language_mode(prompt)

    print(
        f"🌍 AI Mode: {mode}"
    )

    language_instruction = ""

    # ---------------------------------
    # Hinglish
    # ---------------------------------

    if mode == "hinglish":

        language_instruction = """
Reply ONLY in Hinglish.

VERY IMPORTANT:
- Use ONLY English letters
- NO Hindi script
- Natural Hinglish
- Beginner friendly

Example:
"AI ek smart technology hai
jo computer ko seekhne me
madad karti hai."
"""

    # ---------------------------------
    # Hindi
    # ---------------------------------

    elif mode == "hindi":

        language_instruction = """
Reply ONLY in Hindi.

VERY IMPORTANT:
- Use proper Hindi
- No English mix
- Natural Hindi
"""

    # ---------------------------------
    # English
    # ---------------------------------

    elif mode == "english":

        language_instruction = """
Reply ONLY in English.

VERY IMPORTANT:
- Beginner friendly
- Short answer
"""

    # =====================================
    # USER MESSAGE
    # =====================================

    user_message = f"""
{language_instruction}

User:
{prompt}
"""

    conversation_history.append(
        {
            "role": "user",
            "content": user_message
        }
    )

    # =====================================
    # MODEL
    # =====================================

    response = ollama.chat(
        model="qwen2.5:3b",
        messages=conversation_history,
        options={
            "temperature": 0.5,
            "num_predict": 120
        }
    )

    ai_reply = (
        response["message"]["content"]
        .strip()
    )

    # Remove weird quotes
    ai_reply = re.sub(
        r"[“”\"]",
        "",
        ai_reply
    )

    conversation_history.append(
        {
            "role": "assistant",
            "content": ai_reply
        }
    )

    return ai_reply