
import sys
try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except AttributeError:
    pass

from core.listener import listen
import difflib
import re
import time


# ===================================
# CONFIG
# ===================================

WAKE_NAME = "robin"

FUZZY_THRESHOLD = 0.72


# ===================================
# CLEAN TEXT
# ===================================

def clean_text(text):

    text = text.lower().strip()

    # remove punctuation
    text = re.sub(
        r"[^\w\s\u0900-\u097F]",
        "",
        text
    )

    # common whisper fixes
    fixes = {

        "robeen": "robin",
        "robbin": "robin",
        "robinn": "robin",
        "rovin": "robin",
        "gobin": "robin",

        "halo": "hello",
        "hay": "hey",
    }

    for wrong, right in fixes.items():

        text = text.replace(
            wrong,
            right
        )

    return text.strip()


# ===================================
# CHECK WAKE WORD
# ===================================

def is_wake_word(text):

    text = clean_text(text)

    print(f"👂 Heard: {text}")

    words = text.split()

    if not words:
        return False

    # -------------------------
    # direct exact match
    # -------------------------

    if WAKE_NAME in words:
        return True

    # -------------------------
    # phrase match
    # -------------------------

    wake_phrases = {

        "hey robin",
        "hello robin",
        "hi robin",
        "ok robin",
    }

    if text in wake_phrases:
        return True

    # -------------------------
    # fuzzy match
    # -------------------------

    for word in words:

        similarity = difflib.SequenceMatcher(
            None,
            word,
            WAKE_NAME
        ).ratio()

        if similarity >= FUZZY_THRESHOLD:

            print(
                f"🎯 Wake match: "
                f"{word} "
                f"({similarity:.2f})"
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


if __name__ == "__main__":

    while True:

        wait_for_wake_word()

        print("ROBIN Activated")
