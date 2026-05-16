from core.listener import listen


def wait_for_wake_word():

    print("😴 Waiting for wake word...")

    wake_words = [

        "robin",
        "robeen",
        "rabin",
        "robbin",
        "robbin",

        "hello robin",
        "hello robeen",
        "hey robin",
        "hi robin",

        "halo robin",
        "halo robeen",
        "helo robin",

        "robin robin",
        "hello rabin"
    ]

    while True:

        text = listen()

        if not text:
            continue

        text = text.lower().strip()

        print("👂 Heard:", text)

        # Fuzzy matching
        if any(
            wake in text
            for wake in wake_words
        ):

            print(
                "🔔 Wake word detected!"
            )

            return

        # Backup detection
        if (
            "rob" in text
            or "bin" in text
            or "been" in text
            or "robe" in text
        ):

            print(
                "🔔 Wake word detected!"
            )

            return