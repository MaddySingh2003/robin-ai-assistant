import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except AttributeError:
    pass

import time
from tools.command import create_project_file

from core.listener import listen
from core.brain import ask_api_stream
import core.brain

from core.speaker import speak
from core.wake_word import wait_for_wake_word
from assistant.router import route_request

from core.memory import (
    remember,
    recall
)

from core.memory_manager import (
    auto_save_memory
)

from core.code_manager import (
    generate_code_snippet
)


# =====================================
# STARTUP
# =====================================

print("ROBIN: Hello! I'm ROBIN, your AI assistant.")
print("Say 'exit' to quit\n")


# =====================================
# SIMPLE REPLIES
# =====================================

simple_replies = {

    "hello": "Hello boss!",

    "hi": "Hi boss!",

    "hello robin": "Hello boss!",

    "hey robin": "Yes boss?",

    "thank you": "Welcome boss.",

    "thanks": "No problem boss.",

    "good morning": "Good morning boss!",

    "good night": "Good night boss!",

    "kaise ho": "Main badhiya hu boss.",

    "kya haal hai": "Main theek hu boss, aap batao?"
}


# =====================================
# EXIT WORDS
# =====================================

exit_words = [

    "exit",
    "quit",
    "close robin",
    "bye robin",
    "bye bye robin",
    "goodbye robin",
    "turn off robin"
]


# =====================================
# SLEEP WORDS
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
# CLEAN TEXT
# =====================================


def clean_user_text(text):

    text = text.lower().strip()

    fixes = {

        "pythin": "python",
        "wyton": "python",
        "wythin": "python",

        "explainkr": "explain kar",
        "explain kro": "explain karo",

        "grom": "chrome",
        "rome": "chrome",

        "vs code": "vscode",
        "v s code": "vscode",

        "holo": "kholo",
        "kolo": "kholo"
    }

    for wrong, right in fixes.items():
        text = text.replace(
            wrong,
            right
        )

    print(f"🧹 Cleaned: {text}")

    return text.strip()


# =====================================
# BUILD PROMPT
# =====================================

def build_prompt(text, clean_text):

    hinglish_keywords = [

        "hinglish",
        "batao",
        "samjhao",
        "samjha",
        "kya",
        "kaise",
        "kar",
        "karo",
        "kr",
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

User:
{text}
"""

    return text


# =====================================
# CODE REQUEST DETECTION
# =====================================

def is_code_request(text):

    keywords = [

        "write code",
        "generate code",
        "python code",
        "javascript code",
        "html code",
        "css code",
        "create function",
        "make function",
        "create class"
    ]

    return any(
        key in text
        for key in keywords
    )


# =====================================
# MAIN LOOP
# =====================================

try:

    while True:

        wait_for_wake_word()

        speak("Yooohoo")

        time.sleep(0.3)

        while True:

            text = None

            for _ in range(3):

                text = listen()

                if text:
                    break

                print("Retry listening...")

            if not text:

                speak("Going to sleep boss.")

                break

            text = text.strip()

            print("You:", text)

            clean_text = clean_user_text(text)

            # ==========================
            # EXIT
            # ==========================

            if any(
                word in clean_text
                for word in exit_words
            ):

                speak("Goodbye boss")

                print("ROBIN: Goodbye!")

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
            # SIMPLE REPLIES
            # ==========================

            if clean_text in simple_replies:

                response = simple_replies[
                    clean_text
                ]

                print(
                    "ROBIN:",
                    response
                )

                speak(response)

                continue

            # ==========================
            # COMMANDS
            # ==========================\
            
            if ("create" in clean_text and "python file" in clean_text):
                filename = "python.py"

                with open(filename,"w",encoding="utf-8") as f:
                 f.write('# Created by ROBIN\n\nprint("Hello World")')

                 response = ( f"Created {filename}")


                print("ROBIN:", response)

                speak(response)

                continue

            result = route_request(
                clean_text
            )

            if result["type"] == "command":

                response = result.get(
                    "response"
                )

                if response:

                    print(
                        "ROBIN:",
                        response
                    )

                    speak(response)

                continue

            # ==========================
            # CODE REQUEST
            # ==========================

            if is_code_request(
                clean_text
            ):

                code = generate_code_snippet(
                    clean_text
                )

                print(
                    "ROBIN:",
                    code
                )

                speak(
                    "Code generated boss."
                )

                continue

            # ==========================
            # MEMORY RECALL
            # ==========================
            if ("create" in clean_text and "file" in clean_text):
                result = create_project_file(clean_text )
                if result:

                  print("ROBIN:", result)

                  speak(result)

                  continue

            if "your name" in clean_text:

                 speak(
        "My name is Robin."
    )

                 continue

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
            # AUTO SAVE FACTS TO CHROMA
            # ==========================

            auto_save_memory(
                clean_text
            )

            # ==========================
            # AI MODE
            # ==========================

            final_prompt = build_prompt(
                text,
                clean_text
            )

            print(
                "ROBIN:",
                end=" ",
                flush=True
            )

            for sentence in ask_api_stream(
                final_prompt
            ):

                print(
                    sentence,
                    end=" ",
                    flush=True
                )

                speak(
                    sentence,
                    language=core.brain.CURRENT_MODE
                )

            print()

except KeyboardInterrupt:

    print(
        "\nROBIN: Shutting down. Goodbye!"
    )