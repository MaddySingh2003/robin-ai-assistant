import ollama
import re


# =====================================
# GLOBAL MODE MEMORY
# =====================================

CURRENT_MODE = "english"

MAX_HISTORY = 8
LAST_MODE = "english"

# =====================================
# SYSTEM PROMPT
# =====================================

SYSTEM_PROMPT = """
You are ROBIN, a smart female AI assistant.

STRICT RULES:

1. You are FEMALE.
Speak naturally like a female assistant.

Examples:
"I can help."
"Main help kar sakti hu"

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
(1–2 sentences max)

5. Talk naturally like Siri/Jarvis.

HINGLISH RULES:
- Hindi ONLY in English letters
- NEVER Hindi script
- Natural Indian style
- Beginner friendly

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

    # Hindi script → Hinglish
    if re.search(r'[\u0900-\u097F]', text):
        return "hinglish"

    # split words properly
    words = set(re.findall(r'\b\w+\b', text))

    # ==========================
    # HINGLISH WORDS
    # ==========================

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
        "samjhao",
        "batao",
        "hai",
        "ho",
        "hoo",
        "nahi",
        "sakta",
        "sakti",
        "matlab",
        "yeh"
    }

    # Exact word match only
    if words.intersection(hinglish_words):
        return "hinglish"

    # Hinglish phrases
    hinglish_phrases = [

        "explain karo",
        "explain kro",
        "python ko",
        "ke bare me"
    ]

    if any(
        phrase in text
        for phrase in hinglish_phrases
    ):
        return "hinglish"

    # ==========================
    # ENGLISH
    # ==========================

    english_phrases = [

        "what is",
        "who is",
        "where is",
        "when is",
        "why",
        "how",
        "tell me",
        "can you",
        "in english"
    ]

    if any(
        phrase in text
        for phrase in english_phrases
    ):
        return "english"

    return "english"

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

    text = re.sub(
        r'[\u0900-\u097F]',
        "",
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

    mode = detect_language_mode(prompt)

    print(f"🌍 Mode switched → {mode}")

    # =================================
    # RESET MEMORY ON MODE CHANGE
    # =================================

    if mode != LAST_MODE:

        print("♻️ Resetting language memory")

        conversation_history = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ]

    LAST_MODE = mode
    CURRENT_MODE = mode

    # =================================
    # STRICT LANGUAGE INSTRUCTION
    # =================================

    if mode == "english":

        language_instruction = """
You MUST reply ONLY in ENGLISH.

STRICT RULES:
- NO Hindi
- NO Hinglish
- NO Hindi words
- Short answer
- Beginner friendly

Example:
Python is a programming language.

BAD:
Python ek programming language hai.
"""

    else:

        language_instruction = """
You MUST reply ONLY in Hinglish.

STRICT RULES:
- Hindi written ONLY in English letters
- NEVER Hindi script
- NEVER pure English
- ALWAYS mix Hindi + English naturally
- Sound like an Indian assistant
- Short answer

GOOD:
"Python ek programming language hai jo coding easy banati hai."

GOOD:
"Python AI, websites aur automation me use hota hai."

BAD:
"Python is a programming language."

BAD:
"पायथन एक programming language है"
"""

    conversation_history.append(
        {
            "role": "user",
            "content":
            f"{language_instruction}\n\nUser: {prompt}"
        }
    )

    try:

        response = ollama.chat(
            model="qwen2.5:7b",
            messages=conversation_history,
            options={
                "temperature": 0.05,
                "top_p": 0.4,
                "num_predict": 40,
                "repeat_penalty": 1.3
            }
        )

        ai_reply = (
            response["message"]["content"]
            .strip()
        )

        print("🤖 Raw:", ai_reply)

        ai_reply = clean_response(
            ai_reply
        )

        # =================================
        # HARD LANGUAGE ENFORCEMENT
        # =================================

        if mode == "english":

            hinglish_words = {
    "hai",
    "kya",
    "kar",
    "nahi",
    "tum",
    "mera",
    "sakta",
    "sakti",
    "ka",
    "ki",
    "ko"
}

        reply_words = set(
            re.findall(
            r'\b\w+\b',
            ai_reply.lower()
    )
)

        wrong_language = bool(
          reply_words.intersection(
        hinglish_words
    )
)

        if any(
                x in ai_reply.lower()
                for x in hinglish_words
            ):

                print(
                    "⚠️ Wrong language fixed"
                )

                ai_reply = (
                    "Python is a programming language."
                    if "python" in prompt.lower()
                    else "I can help with that."
                )

        else:

            english_only_words = [
                "programming language used for",
                "widely used",
                "high-level"
            ]

            if any(
                x in ai_reply.lower()
                for x in english_only_words
            ):

                ai_reply = (
                    "Python ek programming language hai jo coding easy banati hai."
                )

        # save memory
        conversation_history.append(
            {
                "role": "assistant",
                "content": ai_reply
            }
        )

        return ai_reply

    except Exception as e:

        print("❌ Brain error:", e)

        return (
            "Sorry, something went wrong."
        )