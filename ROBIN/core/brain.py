import ollama
import re


# =====================================
# GLOBALS
# =====================================

CURRENT_MODE = "english"
LAST_MODE = "english"

MAX_HISTORY = 8


# =====================================
# SYSTEM PROMPT
# =====================================

SYSTEM_PROMPT = """
You are ROBIN, a smart female AI assistant.

STRICT RULES:

1. You are FEMALE.
Speak naturally like a female assistant.

2. ONLY support:
- English
- Hinglish

3. NEVER reply in:
- Hindi script
- Spanish
- French
- Korean
- Random languages

4. Keep replies SHORT.
(1-2 sentences max)

5. Talk naturally like Siri/Jarvis.

6. Beginner friendly.

HINGLISH RULES:
- Hindi ONLY in English letters
- NEVER Hindi script
- Natural Indian style

GOOD:
"Python ek programming language hai jo coding easy banati hai."

BAD:
"Python ke liye explain karega."

BAD:
"पायथन ek language hai"
"""


conversation_history = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT
    }
]


# =====================================
# LANGUAGE DETECTION
# =====================================

def detect_language_mode(text):

    text = text.lower().strip()

    # Hindi script → Hinglish
    if re.search(r'[\u0900-\u097F]', text):
        return "hinglish"

    words = set(
        re.findall(
            r'\b\w+\b',
            text
        )
    )

    hinglish_words = {

        "kya",
        "kaise",
        "kyun",
        "tum",
        "aap",
        "mujhe",
        "mera",
        "ko",
        "kar",
        "karo",
        "kr",
        "hai",
        "ho",
        "nahi",
        "sakta",
        "sakti",
        "samjhao",
        "batao",
        "matlab",
        "yeh",
        "ek",
        "ki",
        "ka"
    }

    if words.intersection(
        hinglish_words
    ):
        return "hinglish"

    hinglish_phrases = [

        "ko explain",
        "explain karo",
        "explain kro",
        "ke bare me",
        "ka matlab"
    ]

    if any(
        phrase in text
        for phrase in hinglish_phrases
    ):
        return "hinglish"

    return "english"


# =====================================
# CLEAN RESPONSE
# =====================================

def clean_response(text):

    # Remove code blocks
    text = re.sub(
        r"```.*?```",
        "",
        text,
        flags=re.DOTALL
    )

    # Remove quotes
    text = re.sub(
        r'[\"“”]',
        "",
        text
    )

    # Remove Hindi script
    text = re.sub(
        r'[\u0900-\u097F]',
        "",
        text
    )

    # Remove extra spaces
    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# =====================================
# ASK AI
# =====================================

def ask_api(prompt):

    global CURRENT_MODE
    global LAST_MODE
    global conversation_history

    mode = detect_language_mode(
        prompt
    )

    print(
        f"🌍 Mode switched → {mode}"
    )

    # =================================
    # RESET MEMORY ON LANGUAGE CHANGE
    # =================================

    if mode != LAST_MODE:

        print(
            "♻️ Resetting language memory"
        )

        conversation_history = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ]

    LAST_MODE = mode
    CURRENT_MODE = mode

    # =================================
    # LANGUAGE INSTRUCTIONS
    # =================================

    if mode == "english":

        language_instruction = """
Reply ONLY in ENGLISH.

STRICT RULES:
- NO Hindi
- NO Hinglish
- Short answer
- Beginner friendly

GOOD:
Python is a programming language.

BAD:
Python ek programming language hai.
"""

    else:

        language_instruction = """
Reply ONLY in HINGLISH.

STRICT RULES:
- Hindi in English letters ONLY
- NEVER Hindi script
- Natural Indian style
- Short answer

GOOD:
Python ek programming language hai jo coding easy banati hai.

BAD:
Python is a programming language.
"""

    # =================================
    # SAVE USER MESSAGE
    # =================================

    conversation_history.append(
        {
            "role": "user",
            "content":
            f"{language_instruction}\n\nUser: {prompt}"
        }
    )

    # Keep history short
    if len(conversation_history) > MAX_HISTORY:

        conversation_history = (
            conversation_history[:1]
            + conversation_history[-MAX_HISTORY:]
        )

    try:

        response = ollama.chat(
            model="qwen2.5:7b",
            messages=conversation_history,
            options={
                "temperature": 0.1,
                "top_p": 0.5,
                "num_predict": 50,
                "repeat_penalty": 1.2
            }
        )

        ai_reply = (
            response["message"]["content"]
            .strip()
        )

        print(
            "🤖 Raw:",
            ai_reply
        )

        ai_reply = clean_response(
            ai_reply
        )

        # =================================
        # LANGUAGE ENFORCEMENT
        # =================================

        hinglish_words = {

            "hai",
            "kar",
            "karo",
            "ko",
            "ki",
            "ka",
            "ek",
            "hota",
            "hoti",
            "madad",
            "banati",
            "samjhao",
            "batao",
            "aap",
            "tum",
            "main",
            "sakta",
            "sakti"
        }

        reply_words = set(
            re.findall(
                r'\b\w+\b',
                ai_reply.lower()
            )
        )

        # ---------------------------------
        # ENGLISH MODE
        # ---------------------------------

        if mode == "english":

            wrong_language = bool(
                reply_words.intersection(
                    hinglish_words
                )
            )

            if wrong_language:

                print(
                    "⚠️ Wrong language fixed"
                )

                if "python" in prompt.lower():

                    ai_reply = (
                        "Python is a programming language used for coding."
                    )

                elif "api" in prompt.lower():

                    ai_reply = (
                        "An API helps software communicate with each other."
                    )

                else:

                    ai_reply = (
                        "I can help with that."
                    )

        # ---------------------------------
        # HINGLISH MODE
        # ---------------------------------

        else:

            english_only_patterns = [

                "programming language",
                "widely used",
                "high-level",
                "easy to learn"
            ]

            pure_english = any(
                x in ai_reply.lower()
                for x in english_only_patterns
            )

            if pure_english:

                print(
                    "⚠️ Fixing English → Hinglish"
                )

                if "python" in prompt.lower():

                    ai_reply = (
                        "Python ek programming language hai jo coding easy banati hai."
                    )

                elif "api" in prompt.lower():

                    ai_reply = (
                        "API ek system hai jo apps ko ek dusre se baat karne deta hai."
                    )

                else:

                    ai_reply = (
                        "Main help kar sakti hu."
                    )

        # =================================
        # SAVE MEMORY
        # =================================

        conversation_history.append(
            {
                "role": "assistant",
                "content": ai_reply
            }
        )

        return ai_reply

    except Exception as e:

        print(
            "❌ Brain error:",
            e
        )

        return (
            "Sorry, something went wrong."
        )