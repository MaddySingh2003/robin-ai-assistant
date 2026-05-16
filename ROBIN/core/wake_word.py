from core.listener import listen
import difflib
import re
import time


# ===================================
# WAKE WORDS
# ===================================

WAKE_WORDS = [

    "robin",
    "hey robin",
    "hello robin",
    "hi robin",

    # common whisper mistakes
    "robeen",
    "robin robin",
    "robinn",
    "robbin",
    "robin boss",
    "hello र बन",
    "halo robin",
    "halo robeen",
    "hey robbin",
    "rovin",
    "gobin",
]

# Hindi phonetic versions

HINDI_PATTERNS = [

    "रॉबिन",
    "रोबिन",
    "र बन",
    "रबन",
]


# ===================================
# NORMALIZE TEXT
# ===================================

def clean_text(text):

    text = text.lower()

    text = re.sub(
        r"[^a-zA-Z\u0900-\u097F\s]",
        "",
        text
    )

    return text.strip()


# ===================================
# CHECK WAKE WORD
# ===================================

def is_wake_word(text):

    text = clean_text(text)

    print(f"👂 Heard: {text}")

    # direct match

    for wake in WAKE_WORDS:

        if wake in text:
            return True

    # hindi match

    for word in HINDI_PATTERNS:

        if word in text:
            return True

    # fuzzy match

    words = text.split()

    for word in words:

        similarity = difflib.SequenceMatcher(
            None,
            word,
            "robin"
        ).ratio()

        if similarity > 0.65:
            print(
                f"🎯 Similar word matched: {word}"
            )
            return True

    return False


# ===================================
# WAIT FOR WAKE WORD
# ===================================

def wait_for_wake_word():

    print(
        "😴 Waiting for wake word..."
    )

    while True:

        text = listen()

        if not text:
            continue

        if is_wake_word(text):

            print(
                "🔔 Wake word detected!"
            )

            return

        time.sleep(0.2)