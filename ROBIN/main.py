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


# -------------------
# Simple Hinglish Chat
# -------------------

simple_replies = {

    "kya haal hai":
        "Main theek hoon boss, aap batao?",

    "kaise ho":
        "Main badhiya hoon boss.",

    "hello":
        "Hello boss!",

    "hi":
        "Hi boss!",

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


try:

    while True:

        # -------------------
        # Wake Word
        # -------------------

        wait_for_wake_word()

        speak("Yes boss?")
        time.sleep(1.5)

        # -------------------
        # Listen Command
        # -------------------

        text = None

        for _ in range(3):

         text = listen()

         if text:
           break

         print("Retry listening...")

        if not text:
          speak(
        "I didn't hear anything."
    )
          continue

        text = text.strip()

        print("You:", text)

        # -------------------
        # Exit
        # -------------------

        if text.lower() == "exit":

            speak("Goodbye boss")

            print(
                "ROBIN: Goodbye!"
            )

            break

        # -------------------
        # Route Commands
        # -------------------

        result = route_request(text)

        if (
            result["type"]
            == "command"
        ):

            if result["response"]:

                print(
                    "ROBIN:",
                    result["response"]
                )

                speak(
                    result["response"]
                )

            else:

                speak(
                    "Sorry boss, "
                    "I couldn't understand "
                    "that command."
                )

            continue

        # -------------------
        # Simple Hinglish Chat
        # -------------------

        clean_text = (
            text.lower().strip()
        )

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

        # -------------------
        # Hindi Mode
        # -------------------

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

        # Force Hindi/Hinglish
        if (
            "hindi" in clean_text
            or "hinglish" in clean_text
        ):

            text = (
                "Answer in "
                "Hindi/Hinglish: "
                f"{text}"
            )

        # -------------------
        # AI Chat
        # -------------------

        response = ask_api(text)

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