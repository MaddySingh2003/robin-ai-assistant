from core.listener import listen
from core.brain import ask_api
from core.speaker import speak
from assistant.router import route_request
from core.wake_word import wait_for_wake_word
from core.memory import (
    remember,
    recall
)

import time
import sys


# =====================================
# STARTUP
# =====================================

print(
    "ROBIN: Hello! "
    "I'm ROBIN, your AI assistant."
)

print(
    "Say 'exit' to quit\n"
)


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
        "Good night boss!"
}


# =====================================
# EXIT COMMANDS
# =====================================

exit_words = [

    "exit",
    "quit",
    "close robin",
    "bye robin",
    "bye bye robin",
    "goodbye robin",
    "turn off robin",
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
    "ok robin bye",
    "okay robin bye",
    "see you later",
    "talk to you later",
    "ok bye"
]


# =====================================
# CLEAN USER TEXT
# =====================================

def clean_user_text(text):

    text = text.lower().strip()

    fixes = {

        # Python mistakes
        "pythin": "python",
        "wyton": "python",
        "wythin": "python",
        "ayythan": "python",
        "pythons": "python",

        # Explain mistakes
        "explainkr": "explain kar",
        "explain kro": "explain karo",
        "explate": "explain",

        # Hinglish mistakes
        "hingling": "hinglish",
        "hinglis": "hinglish",
        "hingaleish": "hinglish",
        "hing lish": "hinglish",

        # Chrome mistakes
        "grom": "chrome",
        "rome": "chrome",
        "chchrome": "chrome",

        # Speech mistakes
        "holo": "kholo",
        "kolo": "kholo",

        # VSCode
        "vs code": "vscode",
        "v s code": "vscode",
    }

    for wrong, right in fixes.items():

        text = text.replace(
            wrong,
            right
        )

    print(
        f"🧹 Cleaned: {text}"
    )

    return text.strip()


# =====================================
# BUILD PROMPT
# =====================================

def build_prompt(text, clean_text):

    english_keywords = [

        "english",
        "in english",
        "english me",
        "english mein",
        "only english"
    ]

    if any(
        word in clean_text
        for word in english_keywords
    ):

        return f"""
Reply in SIMPLE English.

Rules:
- English only
- Short answer
- Beginner friendly

User:
{text}
"""

    hinglish_keywords = [

        "hinglish",
        "batao",
        "samjhao",
        "samjha",
        "explain karo",
        "kya",
        "tum",
        "aap",
        "kar",
        "karo",
        "kr",
        "ke bare me",
        "python ko"
    ]

    if any(
        word in clean_text
        for word in hinglish_keywords
    ):

        return f"""
Reply in SIMPLE Hinglish.

Rules:
- Hindi in English letters only
- No Hindi script
- Short answer
- Natural Indian style

User:
{text}
"""

    return text


# =====================================
# MAIN LOOP
# =====================================

try:

    while True:

        # ==========================
        # WAIT FOR WAKE WORD
        # ==========================

        wait_for_wake_word()

        speak(
            "Yes boss"
        )

        time.sleep(0.3)

        # ==========================
        # ACTIVE MODE
        # ==========================

        while True:

            text = None

            # Retry listening
            for _ in range(3):

                text = listen()

                if text:
                    break

                print(
                    "Retry listening..."
                )

            # No speech detected
            if not text:

                speak(
                    "Going to sleep boss."
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

            # ==========================
            # EXIT
            # ==========================

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

            # ==========================
            # SLEEP
            # ==========================

            if any(
                word in clean_text
                for word in sleep_words
            ):

                speak(
                    "Going back to sleep boss."
                )

                break

            # ==========================
            # SIMPLE CHAT
            # ==========================

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

                speak(
                    response
                )

                continue

            # ==========================
            # MEMORY RECALL
            # ==========================

            memory_response = recall(
                clean_text
            )

            if memory_response:

                print(
                    "ROBIN:",
                    memory_response
                )

                speak(
                    memory_response
                )

                continue

            # ==========================
            # MEMORY SAVE
            # ==========================

            memory_save = remember(
                clean_text
            )

            if memory_save:

                print(
                    "ROBIN:",
                    memory_save
                )

                speak(
                    memory_save
                )

                continue

            # ==========================
            # COMMAND ROUTER
            # ==========================

            result = route_request(
                clean_text
            )

            print(result)

            if (
                result["type"]
                == "command"
            ):

                response = result.get(
                    "response"
                )

                if response:

                    print(
                        "ROBIN:",
                        response
                    )

                    speak(
                        response
                    )

                else:

                    speak(
                        "Sorry boss, I couldn't understand that command."
                    )

                continue

            # ==========================
            # AI MODE
            # ==========================

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

            speak(
                response
            )

except KeyboardInterrupt:

    print(
        "\nROBIN: Shutting down. Goodbye!"
    )