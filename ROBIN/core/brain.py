import sys
try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except AttributeError:
    pass

import ollama
import re

from core.memory_manager import (
    get_memory_context
)


# =====================================
# GLOBALS
# =====================================

# Configurable model name. "gemma3:1b" runs ultra-fast on CPU systems.
OLLAMA_MODEL = "gemma3:1b"

CURRENT_MODE = "english"
LAST_MODE = "english"

MAX_HISTORY = 8


# =====================================
# SYSTEM PROMPT
# =====================================

SYSTEM_PROMPT = """
You are ROBIN.

IMPORTANT:

You are NOT Gemma.
You are NOT ChatGPT.
You are NOT an AI model.

Your name is ROBIN.

If anyone asks:

"What is your name"

Reply:

"My name is Robin."

Never mention Gemma.
Never mention model names, a smart female AI assistant.

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

7. Use memory when available.

8. If memory contains user facts,
use them naturally.
9. don't use any Emojis in your replies.

HINGLISH RULES:
- Hindi ONLY in English letters
- NEVER Hindi script
Never claim you created a file,
folder,
project,
website,
application,
or code unless the system explicitly tells you it was created.

If you did not actually create it,
say you cannot verify creation.
don't use emojies in any senario.
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

    # Unicode Hindi script detection (covers pure Hindi input)
    if re.search(r'[\u0900-\u097F]', text):
        return "hinglish"

    words = set(re.findall(r"\b\w+\b", text))

    # Unified Hinglish vocabulary (matches speaker.py)
    hinglish_words = {
        "hai", "kar", "karo", "ka", "ki", "ke", "ko", "ek", "kya", "kaise",
        "kyun", "aap", "tum", "mujhe", "mera", "samjhao", "batao", "sakta",
        "sakti", "hu", "aur", "toh", "tha", "thi", "raha", "rahi", "rahe",
        "hoga", "hogi", "hoge", "gaya", "gayi", "gaye", "karta", "karti",
        "karte", "diya", "liya", "kiya", "kijiye", "karke", "chalo", "achha",
        "accha", "badhiya", "theek", "samjha", "kholo", "chalu",
        "niklo", "jao", "aao", "karna", "krna"
    }

    matches = len(words.intersection(hinglish_words))

    # Use a single matching word to consider Hinglish
    if matches >= 1:
        return "hinglish"

    return "english"


# =====================================
# CLEAN RESPONSE
# =====================================

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

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# =====================================
# ASK AI STREAM
# =====================================

def ask_api_stream(prompt):

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
    # RESET ON LANGUAGE CHANGE
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
    # MEMORY SEARCH
    # =================================

    memory_context = get_memory_context(
        prompt
    )

    print(
        f"🧠 Memories Found: "
        f"{len(memory_context.splitlines()) if memory_context else 0}"
    )

    # =================================
    # LANGUAGE RULES
    # =================================

    if mode == "english":

        language_instruction = """
Reply ONLY in ENGLISH.

Rules:
- No Hindi
- No Hinglish
- Short answer
- Beginner friendly
"""

    else:

        language_instruction = """
Reply ONLY in HINGLISH.

Rules:
- Hindi in English letters only
- Never Hindi script
- Natural Indian style
- Short answer
"""

    # =================================
    # USER MESSAGE
    # =================================

    # ===============================
    # MEMORY FILTERING
    # Remove any memory lines that could confuse the assistant about its own name.
    # Specifically, drop lines containing "my name is" as they refer to the user.
    filtered_memory = "\n".join(
        [line for line in memory_context.splitlines() if not re.search(r"\\bmy name is\\b", line.lower())]
    )

    user_content = f"""
{language_instruction}

MEMORY:
{filtered_memory}

USER:
{prompt}
"""

    conversation_history.append(
        {
            "role": "user",
            "content": user_content
        }
    )

    # =================================
    # HISTORY LIMIT
    # =================================

    if len(
        conversation_history
    ) > MAX_HISTORY:

        conversation_history = (
            conversation_history[:1]
            + conversation_history[-MAX_HISTORY:]
        )

    try:

        response_stream = ollama.chat(
            model=OLLAMA_MODEL,
            messages=conversation_history,
            options={
                "temperature": 0.2,
                "top_p": 0.7,
                "num_predict": 80,
                "repeat_penalty": 1.1
            },
            stream=True
        )

        buffer = ""
        full_reply = ""
        sentence_yielded = False

        for chunk in response_stream:

            content = chunk["message"]["content"]
            buffer += content
            full_reply += content

            # Split buffer into sentences on sentence boundaries or newlines
            sentences = re.split(r'(?<=[.!?])\s+|\n+', buffer)

            if len(sentences) > 1:

                for sentence in sentences[:-1]:

                    clean_sent = clean_response(sentence)

                    if clean_sent:

                        # Language enforcement for English mode
                        if mode == "english" and re.search(r'[\u0900-\u097F]', clean_sent):
                            clean_sent = "I can help with that."

                        yield clean_sent
                        sentence_yielded = True

                buffer = sentences[-1]

        # Yield any remaining text in buffer
        if buffer.strip():

            clean_sent = clean_response(buffer)

            if clean_sent:

                if mode == "english" and re.search(r'[\u0900-\u097F]', clean_sent):
                    clean_sent = "I can help with that."

                yield clean_sent
                sentence_yielded = True

        cleaned_full_reply = clean_response(full_reply)

        # Fallback if reply is too short
        if not sentence_yielded or len(cleaned_full_reply.strip()) < 3:

            if mode == "hinglish":
                fallback = "Main help kar sakti hu."
            else:
                fallback = "I can help with that."

            yield fallback
            cleaned_full_reply = fallback

        print(
            "🤖 Full Reply:",
            cleaned_full_reply
        )

        # =================================
        # SAVE ASSISTANT MESSAGE
        # =================================

        conversation_history.append(
            {
                "role": "assistant",
                "content": cleaned_full_reply
            }
        )

    except Exception as e:

        print(
            "❌ Brain error:",
            e
        )

        yield "Sorry, something went wrong."


# =====================================
# ASK AI (COMPATIBILITY WRAPPER)
# =====================================

def ask_api(prompt):

    sentences = list(ask_api_stream(prompt))
    return " ".join(sentences)