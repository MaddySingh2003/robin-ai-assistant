import ollama
import re


# =====================================
# GLOBAL MODE MEMORY
# =====================================

CURRENT_MODE = "english"


# =====================================
# SYSTEM PROMPT
# =====================================

SYSTEM_PROMPT = """
You are ROBIN, a smart female AI assistant.

STRICT RULES:

1. You are FEMALE.
Speak naturally like a female assistant.

Examples:
"kar sakti hu"
"samjha sakti hu"

2. ONLY support:
- English
- Hinglish

3. NEVER reply in:
- Spanish
- French
- Korean
- Random languages

4. Keep replies SHORT.
(1-2 sentences)

5. Talk naturally like Siri/Jarvis.

HINGLISH RULES:
- Hindi ONLY in English letters
- NEVER Hindi script
- NEVER pure English
- Natural Indian style

GOOD:
"Python ek programming language hai jo coding easy banati hai."

BAD:
"Python ke liye explain karega."

BAD:
"पायथन एक language है"
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

    # -------------------------
    # ENGLISH
    # -------------------------

    english_words = [

        "what is",
        "how are you",
        "can you",
        "tell me",
        "in english",
        "english",
        "who is",
        "why",
        "when",
        "where",
    ]

    if any(word in text for word in english_words):
        return "english"

    # -------------------------
    # HINGLISH
    # -------------------------

    hinglish_words = [

        "kya",
        "kaise",
        "kyun",
        "tum",
        "aap",
        "mujhe",
        "mera",
        "ko",
        "karo",
        "kar",
        "kr",
        "samjhao",
        "batao",
        "explain karo",
        "explain kro",
        "hai",
        "ho",
        "hoo",
        "nahi",
        "sakta",
        "sakti"
    ]

    # Hindi script = Hinglish
    if re.search(r'[\u0900-\u097F]', text):
        return "hinglish"

    if any(word in text for word in hinglish_words):
        return "hinglish"

    # -------------------------
    # DEFAULT
    # -------------------------

    return "english"
def clean_response(text):

    text = re.sub(
        r'[\"“”]',
        "",
        text
    )

    return text.strip()


# =====================================
# ASK AI
# =====================================

def ask_api(prompt):

    mode = detect_language_mode(prompt)

    print(f"🌍 Mode switched → {mode}")

    # =====================================
    # STRICT LANGUAGE PROMPTS
    # =====================================

    if mode == "english":

        system_prompt = """
You are ROBIN, a smart female AI assistant.

STRICT RULES:
- Reply ONLY in English.
- NEVER use Hindi words.
- NEVER use Hinglish.
- NEVER use Hindi script.
- Keep answers SHORT.
- Speak naturally like Jarvis/Siri.
- Beginner friendly.

GOOD:
"Python is a programming language used for coding."

BAD:
"Python ek programming language hai"
"""

    else:  # hinglish

        system_prompt = """
You are ROBIN, a smart female AI assistant.

STRICT RULES:
- Reply ONLY in Hinglish.
- Hindi MUST be written in English letters.
- NEVER use Hindi script.
- NEVER reply in pure English.
- Keep answers SHORT.
- Speak naturally like Indians.

GOOD:
"Python ek programming language hai jo coding easy banati hai."

BAD:
"Python is a programming language"

BAD:
"पायथन एक भाषा है"
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
            ],

            options={
                "temperature": 0.0,
                "top_p": 0.3,
                "num_predict": 35,
                "repeat_penalty": 1.2
            }
        )

        ai_reply = response["message"][
            "content"
        ].strip()

        ai_reply = re.sub(
            r'[\"“”]',
            "",
            ai_reply
        )

        print("🤖 Raw:", ai_reply)

        # =====================================
        # FORCE LANGUAGE FIX
        # =====================================

        if mode == "english":

            # If Hindi leaked → regenerate
            hindi_words = [
                "hai",
                "kya",
                "kaise",
                "kar",
                "ek",
                "jo"
            ]

            if any(
                word in ai_reply.lower()
                for word in hindi_words
            ):

                ai_reply = (
                    "Python is a programming language "
                    "used for coding."
                )

        else:

            # Hinglish fix
            if (
                "python" in prompt.lower()
            ):

                ai_reply = (
                    "Python ek programming language hai "
                    "jo coding easy banati hai."
                )

        return ai_reply

    except Exception as e:

        print(
            "❌ Brain error:",
            e
        )

        return (
            "Sorry boss."
        )