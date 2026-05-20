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

    global CURRENT_MODE

    text = text.lower().strip()

    # ---------------------------------
    # FORCE ENGLISH
    # ---------------------------------

    english_words = [

        "english",
        "in english",
        "only english",
        "english me",
        "english mein",
    ]

    if any(
        word in text
        for word in english_words
    ):

        return "english"

    # ---------------------------------
    # HINGLISH
    # ---------------------------------

    hinglish_words = [

        "kya",
        "tum",
        "aap",
        "mujhe",
        "mera",
        "kaise",
        "kyun",

        "batao",
        "samjhao",
        "samjha",
        "explain",
        "karo",
        "kar",
        "kr",

        "sakta",
        "sakti",
        "hai",
        "ho",
        "hoo",
        "nahi",

        "ke bare me",
        "ko explain",
        "python ko",
        "python ke bare me",
        "corro",
        "kro"
    ]

    score = sum(
        word in text
        for word in hinglish_words
    )

    if re.search(r'[\u0900-\u097F]', text):
       return "hinglish"

    if (
    "python ko" in text
    or "explain karo" in text
    or "ko explain" in text
):
      return "hinglish"

    if score >= 1:
       return "hinglish"
    # ---------------------------------
    # KEEP LAST MODE
    # ---------------------------------

    return CURRENT_MODE


# =====================================
# CLEAN RESPONSE
# =====================================

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

    global CURRENT_MODE

    CURRENT_MODE = (
        detect_language_mode(prompt)
    )

    print(
        f"🌍 Mode switched → "
        f"{CURRENT_MODE}"
    )

    # =====================================
    # LANGUAGE INSTRUCTION
    # =====================================

    if CURRENT_MODE == "hinglish":

        language_instruction = """
Reply ONLY in Hinglish.

STRICT RULES:
- Hindi ONLY in English letters
- NEVER Hindi script
- NEVER pure English
- Short answer
- Female speaking style

GOOD:
"Python ek programming language hai jo coding easy banati hai."

GOOD:
"AI computer ko smart banane me help karti hai."

BAD:
"Python ke liye explain karega."
"""

    else:

        language_instruction = """
Reply ONLY in English.

STRICT RULES:
- English ONLY
- Beginner friendly
- Short answer
- No Hindi
"""

    # =====================================
    # MESSAGE
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

    try:

        response = ollama.chat(
            model="qwen2.5:3b",

            messages=conversation_history,

            options={
                "temperature": 0.15,
                "num_predict": 60,
                "top_p": 0.8
            }
        )

        ai_reply = (
            response["message"]["content"]
            .strip()
        )

        ai_reply = clean_response(
            ai_reply
        )

        # block weird languages
        blocked_words = [

            "hola",
            "bonjour",
            "merci",
            "gracias",
            "안녕"
        ]

        if any(
            word in ai_reply.lower()
            for word in blocked_words
        ):

            ai_reply = (
                "Dobara pucho boss."
                if CURRENT_MODE
                == "hinglish"
                else
                "Please ask again."
            )

        # Hinglish safety
        if CURRENT_MODE == "hinglish":

            if re.search(
                r'[\u0900-\u097F]',
                ai_reply
            ):

                ai_reply = (
                    "Dobara pucho boss."
                )

        conversation_history.append(
            {
                "role": "assistant",
                "content": ai_reply
            }
        )

        return ai_reply

    except Exception as e:

        print(
            "❌ Brain Error:",
            e
        )

        return (
            "Sorry boss, try again."
        )