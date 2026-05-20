import ollama
import re


# =====================================
# GLOBAL LANGUAGE MEMORY
# =====================================

CURRENT_MODE = "english"


# =====================================
# SYSTEM PROMPT
# =====================================

SYSTEM_PROMPT = """
You are ROBIN, a smart female AI assistant.
replay as femal assitant "kar satki hu , karti hu ,etc,"

STRICT RULES:

1. NEVER reply in Spanish.
2. NEVER reply in French.
3. NEVER switch languages randomly.
4. Reply SHORT (1-3 sentences only).
5. Speak naturally like Siri/Jarvis.

LANGUAGE RULES:

ENGLISH MODE:
- ONLY English.
- No Hindi words.

HINDI MODE:
- ONLY Hindi script.
- No English words.

HINGLISH MODE:
VERY IMPORTANT:
- ONLY Hindi written in English letters.
- NEVER use Hindi script.
- NEVER use Devanagari.
- NEVER use pure English only.
- Speak like Indians chat.

GOOD:
"Python ek programming language hai jo coding easy banati hai."

BAD:
"Python is a programming language"

BAD:
"पायथन एक प्रोग्रामिंग भाषा है"

Always obey language mode strictly.
"""


conversation_history = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT
    }
]


# =====================================
# DETECT LANGUAGE MODE
# =====================================

def detect_language_mode(text):

    text = text.lower().strip()

    # =====================================
    # HINGLISH KEYWORDS
    # =====================================

    hinglish_keywords = [

        "hinglish",
        "hing lish",
        "hingaleish",
        "hingling",

        "batao",
        "samjhao",
        "samjha",
        "samjhao na",

        "kya",
        "kaise",
        "kyu",
        "kyun",
        "haal",
        "haan",
        "nahi",
        "acha",
        "accha",
        "theek",
        "bhai",
        "boss",
        "mera",
        "tum",
        "aap",
        "kar",
        "karo",
        "kro",
        "bolo",

        "ke bare me",
        "ke baare me",
    ]

    # =====================================
    # ENGLISH MODE COMMANDS
    # =====================================

    english_keywords = [

        "english me",
        "english mein",
        "in english",
        "only english",
        "speak english",
    ]

    if any(word in text for word in english_keywords):

        return "english"

    # =====================================
    # HINDI MODE COMMANDS
    # =====================================

    hindi_keywords = [

        "hindi me",
        "hindi mein",
        "in hindi",
        "only hindi",
    ]

    if any(word in text for word in hindi_keywords):

        return "hindi"

    # =====================================
    # AUTO HINGLISH DETECT
    # =====================================

    hinglish_score = sum(
        word in text
        for word in hinglish_keywords
    )

    if hinglish_score >= 1:
        return "hinglish"

    # =====================================
    # PURE HINDI SCRIPT
    # =====================================

    hindi_script = re.search(
        r'[\u0900-\u097F]',
        text
    )

    if hindi_script:
        return "hindi"

    # =====================================
    # DEFAULT
    # =====================================

    return None

# =====================================
# ASK AI
# =====================================

def ask_api(prompt):

    global CURRENT_MODE

    detected_mode = (
        detect_language_mode(prompt)
    )

    # Save mode permanently

    if detected_mode is not None:

        CURRENT_MODE = (
            detected_mode
        )

        print(
            f"🌍 Mode switched → "
            f"{CURRENT_MODE}"
        )

    print(
        f"🌍 AI Mode: "
        f"{CURRENT_MODE}"
    )

    # =====================================
    # FORCE LANGUAGE
    # =====================================

    if CURRENT_MODE == "hinglish":

        language_instruction = """
Reply ONLY in Hinglish.

STRICT RULES:
- Use English letters only
- NO Hindi script
- NO Spanish
- Natural Hinglish
- Short answer

Example:
"Python ek programming language hai jo coding easy banati hai."
"""

    elif CURRENT_MODE == "hindi":

        language_instruction = """
Reply ONLY in Hindi.

STRICT RULES:
- Only Hindi script
- No English
- Short answer
"""

    else:

        language_instruction = """
Reply ONLY in English.

STRICT RULES:
- No Hindi
- No Spanish
- Beginner friendly
- Short answer
"""

    # =====================================
    # USER MESSAGE
    # =====================================

    user_message = f"""
{language_instruction}

User Question:
{prompt}
"""

    conversation_history.append(
        {
            "role": "user",
            "content": user_message
        }
    )

    # =====================================
    # OLLAMA
    # =====================================

    response = ollama.chat(
        model="qwen2.5:3b",
        messages=conversation_history,
        options={
            "temperature": 0.2,
            "num_predict": 80,
            "top_p": 0.8
        }
    )

    ai_reply = (
        response["message"]["content"]
        .strip()
    )

    # Clean weird symbols
    ai_reply = re.sub(
        r"[\"“”]",
        "",
        ai_reply
    )

    # =====================================
    # FORCE FIXES
    # =====================================

    # Hinglish accidentally in Hindi
    if CURRENT_MODE == "hinglish":

        hindi_chars = re.search(
            r'[\u0900-\u097F]',
            ai_reply
        )

        if hindi_chars:

            ai_reply = (
                "Sorry boss, "
                "dobara pucho."
            )

    # English accidentally Spanish
    spanish_words = [
        "hola",
        "gracias",
        "quieres",
        "lenguaje",
        "programación"
    ]

    if CURRENT_MODE == "english":

        if any(
            word in ai_reply.lower()
            for word in spanish_words
        ):

            ai_reply = (
                "Sorry boss, "
                "please ask again."
            )

    conversation_history.append(
        {
            "role": "assistant",
            "content": ai_reply
        }
    )

    return ai_reply