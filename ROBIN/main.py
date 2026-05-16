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
        "Main theek hoon boss, aap batao?",

    "kaise ho":
        "Main badhiya hoon boss.",

    "hello":
        "Hello boss!",

    "hi":
        "Hi boss!",

    "hello robin":
        "Hello boss!",

    "hey robin":
        "Yes boss?",

    "namaste":
        "Namaste boss!",

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
    "shutdown",
    "shut down",
    "turn off",
    "close robin",
    "bye robin",
    "bye bye robin",
    "goodbye robin",
    "ok robin bye",
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
# LANGUAGE MODE
# =====================================

def build_prompt(text, clean_text):

    # Hinglish Mode
    if (
        "in hinglish" in clean_text
        or "hinglish me" in clean_text
        or "hinglish mein" in clean_text
        or "explain in hinglish" in clean_text
    ):

        return f"""
Explain in SIMPLE Hinglish.

STRICT RULES:
- Hindi written ONLY in English letters
- NEVER use Hindi script
- NEVER use Devanagari
- Speak naturally like Indians
- Keep response short
- Beginner friendly

Question:
{text}
"""

    # Hindi Mode
    elif (
        "in hindi" in clean_text
        or "hindi me" in clean_text
        or "hindi mein" in clean_text
        or "explain in hindi" in clean_text
    ):

        return f"""
Explain ONLY in Hindi.

STRICT RULES:
- Use ONLY Hindi language
- Natural Hindi
- No English
- Short answer
- Beginner friendly

Question:
{text}
"""

    # English Mode
    elif (
        "in english" in clean_text
        or "english me" in clean_text
        or "english mein" in clean_text
        or "explain in english" in clean_text
    ):

        return f"""
Explain in SIMPLE English.

STRICT RULES:
- Beginner friendly
- Short explanation
- Natural English
- Voice assistant style

Question:
{text}
"""

    return text


# =====================================
# MAIN LOOP
# =====================================

try:

    while True:

        # =====================================
        # WAIT FOR WAKE WORD
        # =====================================

        wait_for_wake_word()

        # better sounding
        speak("Ji boss?")

        time.sleep(0.5)

        # =====================================
        # ACTIVE LISTENING MODE
        # =====================================

        while True:

            text = None

            # Retry 3 times
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

            clean_text = (
                text.lower().strip()
            )

            # =====================================
            # EXIT ROBIN
            # =====================================

            if any(
                word in clean_text
                for word in exit_words
            ):

                speak(
                    "Goodbye boss."
                )

                print(
                    "ROBIN: Goodbye!"
                )

                sys.exit()

            # =====================================
            # GO TO SLEEP
            # =====================================

            if any(
                word in clean_text
                for word in sleep_words
            ):

                speak(
                    "Going back to sleep boss."
                )

                break

            # =====================================
            # SIMPLE CHAT
            # =====================================

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

            # =====================================
            # COMMANDS
            # =====================================

            result = (
                route_request(text)
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

            # =====================================
            # AI MODE
            # =====================================

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