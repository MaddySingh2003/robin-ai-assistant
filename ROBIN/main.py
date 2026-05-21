from core.listener import listen
from core.brain import ask_api
from core.speaker import speak
from assistant.router import route_request
from core.wake_word import wait_for_wake_word

import time
import sys


# =====================================
# STARTUP
# =====================================

print(
    "ROBIN: Hello! "
    "I'm ROBIN, your AI assistant."
)

print("Say 'exit' to quit\n")


# =====================================
# SIMPLE REPLIES
# =====================================

simple_replies = {

    "kya haal hai":
        "Main theek hu boss, aap batao?",

    "kaise ho":
        "Main badhiya hu boss.",

    "hello":
        "Hello boss!",

    "hi":
        "Hi boss!",

    "hello robin":
        "Hello boss!",

    "hey robin":
        "Yes boss?",

    "thank you":
        "Welcome boss.",

    "thanks":
        "No problem boss.",

    "good morning":
        "Good morning boss!",

    "good night":
        "Good night boss!",
}


# =====================================
# EXIT COMMANDS
# =====================================

exit_words = [

    "exit",
    "quit",
    "shutdown",
    "shut down",
    "turn off",
    "close robin",
    "bye robin",
    "bye bye robin",
    "goodbye robin",
    "ok robin bye",
    "okay robin bye",
    "ok bye"
]


# =====================================
# SLEEP COMMANDS
# =====================================

sleep_words = [

    "sleep",
    "go to sleep",
    "stop listening",
    "nothing else",
    "no more",
    "see you later",
    "talk to you later",
]


# =====================================
# CLEAN USER TEXT
# =====================================

def clean_user_text(text):

    text = text.lower().strip()

    fixes = {

        # Python mistakes
        "pythin": "python",
        "pythin": "python",
        "pythin'": "python",
        "wyton": "python",
        "wythin": "python",
        "ayythan": "python",
        "pythons": "python",

        # explain mistakes
        "explainkr": "explain kar",
        "explain kro": "explain karo",
        "explate": "explain",

        # hinglish mistakes
        "hingling": "hinglish",
        "hinglis": "hinglish",
        "hingaleish": "hinglish",
        "hing lish": "hinglish",

        # chrome mistakes
        "grom": "chrome",
        "rome": "chrome",
        "holo": "kholo",
        "kolo": "kholo",
    }

    for wrong, right in fixes.items():

        text = text.replace(
            wrong,
            right
        )

    print(
        f"🧹 Cleaned: {text}"
    )

    return text


# =====================================
# BUILD PROMPT
# =====================================

def build_prompt(text, clean_text):

    # ---------------------
    # English Mode
    # ---------------------

    english_keywords = [

        "english",
        "in english",
        "english me",
        "english mein",
        "explain in english",
        "only english",
    ]

    if any(
        word in clean_text
        for word in english_keywords
    ):

        return f"""
Explain in SIMPLE English.

STRICT RULES:
- English only
- Short answer
- Beginner friendly
- Natural voice assistant

Question:
{text}
"""

    # ---------------------
    # Hinglish Mode
    # ---------------------

    hinglish_keywords = [

        "hinglish",
        "hinglish me",
        "hinglish mein",
        "batao",
        "samjhao",
        "samjha",
        "explain karo",
        "explain kro",
        "kya",
        "tum",
        "aap",
        "kar",
        "karo",
        "kr",
        "sakta",
        "sakti",
        "ke bare me",
        "python ko",
    ]

    if any(
        word in clean_text
        for word in hinglish_keywords
    ):

        return f"""
Explain in SIMPLE Hinglish.

STRICT RULES:
- Hindi ONLY in English letters
- NEVER Hindi script
- NEVER pure English
- Natural Indian style
- Short answer
- Female assistant speaking style

Question:
{text}
"""

    return text


# =====================================
# MAIN LOOP
# =====================================

try:

    while True:

        # ==============================
        # WAIT FOR WAKE WORD
        # ==============================

        wait_for_wake_word()

        speak("Yes boss")

        time.sleep(0.3)

        # ==============================
        # ACTIVE MODE
        # ==============================

        while True:

            text = None

            # retry 3 times
            for _ in range(3):

                text = listen()

                if text:
                    break

                print(
                    "Retry listening..."
                )

            # No speech
            if not text:

                speak(
                    "Going back to sleep boss."
                )

                break

            text = text.strip()

            print(
                "You:",
                text
            )

            clean_text = clean_user_text(
                text
            )

            # ==============================
            # EXIT
            # ==============================

            if any(
                word in clean_text
                for word in exit_words
            ):

                speak(
                    "Goodbye boss"
                )

                print(
                    "ROBIN: Goodbye!"
                )

                sys.exit()

            # ==============================
            # SLEEP
            # ==============================

            if any(
                word in clean_text
                for word in sleep_words
            ):

                speak(
                    "Going back to sleep boss."
                )

                break

            # ==============================
            # SIMPLE CHAT
            # ==============================

            if clean_text in simple_replies:

                response = (
                    simple_replies[
                        clean_text
                    ]
                )

                print(
                    "ROBIN:",
                    response
                )

                speak(response)

                continue

            # ==============================
            # COMMAND ROUTER
            # ==============================

            result = route_request(
                clean_text
            )

            print(result)

            if (
                result["type"]
                == "command"
            ):

                response = (
                    result.get(
                        "response"
                    )
                )

                if response:

                    print(
                        "ROBIN:",
                        response
                    )

                    speak(response)

                else:

                    speak(
                        "Sorry boss, "
                        "I couldn't "
                        "understand "
                        "that command."
                    )

                continue

            # ==============================
            # AI MODE
            # ==============================

            final_prompt = build_prompt(
                text,
                clean_text
            )

            response = ask_api(
                final_prompt
            )

            print(
                "ROBIN:",
                response
            )

            speak(response)

except KeyboardInterrupt:

    print(
        "\nROBIN: "
        "Shutting down. Goodbye!"
    )