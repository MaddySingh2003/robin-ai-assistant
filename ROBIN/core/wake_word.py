from core.listener import listen


WAKE_WORDS=[   "robin",
    "hello robin",
    "hey robin",
    "hi robin",

    # Whisper mistakes
    "rabin",
    "robbin",
    "robin robin",
    "hallow robin",
    "halu robin",
    "hello rabin"
]

def wait_for_wake_word():
    
    print("😴 Waiting for wake word...")

    while True:

        text=listen()
        if not text:
            continue

        text=text.lower().strip()

        print(f"👂 Heard: {text}")

        for wake_word in WAKE_WORDS:
            if wake_word in text:
                print("🔔 Wake word detected!")
                return True