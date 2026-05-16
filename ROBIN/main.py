from core.listener import listen
from core.brain import ask_api
from core.speaker import speak
from assistant.router import route_request
from core.wake_word import wait_for_wake_word
import time


print(
    "ROBIN: Hello! "
    "I'm ROBIN, your AI assistant."
)

print("Say 'exit' to quit\n")


# =====================================
# SIMPLE HINGLISH CHAT
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
        "Good night boss.",

    "bye":
        "Bye boss, take care!"
}


# =====================================
# EXIT WORDS
# =====================================

sleep_words = [

    "bye",
    "goodbye",
    "go to sleep",
    "sleep",
    "see you later",
    "talk to you later",
    "stop",
    "nothing else",
    "no more",
    "i am done",
    "thanks",
    "thank you"
]

exit_words = [

    "exit",
    "quit",
    "shutdown",
    "shut down",
    "turn off"
]


try:

    while True:

        # =====================================
        # WAIT FOR WAKE WORD
        # =====================================

        wait_for_wake_word()

        speak("Yes boss?")
        time.sleep(1)

        # =====================================
        # ACTIVE MODE
        # =====================================

        while True:

            text = None

            # Try listening 3 times
            for _ in range(3):

                text = listen()

                if text:
                    break

                print(
                    "Retry listening..."
                )

            # Nothing heard
            if not text:

                speak(
                    "Going back to sleep."
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
            # EXIT APP
            # =====================================

            if clean_text in exit_words:

                speak(
                    "Goodbye boss"
                )

                print(
                    "ROBIN: Goodbye!"
                )

                exit()

            # =====================================
            # GO TO SLEEP
            # =====================================

            if clean_text in sleep_words:

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
            # COMMAND ROUTER
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
                        "I could not "
                        "understand "
                        "that command."
                    )

                continue

            # =====================================
            # HINDI MODE
            # =====================================

            if (

                "talk to me in hindi"
                in clean_text

                or "speak hindi"
                in clean_text

                or "hindi me baat karo"
                in clean_text
            ):

                response = (
                    "ठीक है बॉस, "
                    "अब मैं हिंदी में "
                    "बात करूँगा।"
                )

                print(
                    "ROBIN:",
                    response
                )

                speak(response)

                continue

            # Force Hindi / Hinglish

            if (
                "hindi"
                in clean_text

                or "hinglish"
                in clean_text
            ):

                text = (
                    "Answer in "
                    "Hindi/Hinglish: "
                    f"{text}"
                )

            # =====================================
            # AI CHAT
            # =====================================

            response = (
                ask_api(text)
            )

            print(
                "ROBIN:",
                response
            )

            speak(response)


except KeyboardInterrupt:

    print(
        "\nROBIN: "
        "Shutting down. "
        "Goodbye!"
    )