import subprocess
import os
import time
import uuid
import pygame
import re


# ==========================
# PIPER CONFIG
# ==========================

PIPER_PATH = (
    r"D:\AI-Assistant\piper\piper.exe"
)

ENGLISH_MODEL = (
    r"D:\AI-Assistant\piper\models"
    r"\en_US-amy-medium.onnx"
)

HINDI_MODEL = (
    r"D:\AI-Assistant\piper\models"
    r"\hi_IN-priyamvada-medium.onnx"
)


# ==========================
# INIT PYGAME
# ==========================

pygame.mixer.init()


# ==========================
# LANGUAGE DETECTION
# ==========================

def detect_language(text):

    text_lower = text.lower()

    # ----------------------
    # Hindi script detection
    # ----------------------

    hindi_script = re.search(
        r'[\u0900-\u097F]',
        text
    )

    if hindi_script:
        return "hindi"

    # ----------------------
    # Hinglish detection
    # ----------------------

    hinglish_words = [

        "hai",
        "haan",
        "nahi",
        "kya",
        "kaise",
        "kyun",
        "kar",
        "samjho",
        "samjhao",
        "batao",
        "seekho",
        "samajh",
        "theek",
        "acha",
        "bhai",
        "boss",
        "mera",
        "tum",
        "aap",
        "matlab",
        "karna",
        "bolo",
        "explain in hinglish",
        "hinglish"
    ]

    if any(
        word in text_lower
        for word in hinglish_words
    ):
        return "hinglish"

    return "english"


# ==========================
# SPEAK
# ==========================

def speak(text):

    if not text:
        return

    print("ROBIN:", text)

    output_file = (
        f"voice_"
        f"{uuid.uuid4().hex[:8]}.wav"
    )

    # ----------------------
    # Detect language
    # ----------------------

    language = detect_language(text)

    print(
        f"Detected language: "
        f"{language}"
    )

    # ----------------------
    # Select voice
    # ----------------------

    if language == "hindi":

        model = HINDI_MODEL

        print(
            "Using Hindi voice"
        )

    elif language == "hinglish":

        # Hinglish sounds better
        # with English voice
        model = ENGLISH_MODEL

        print(
            "Using Hinglish "
            "(Hindi) voice"
        )

    else:

        model = ENGLISH_MODEL

        print(
            "Using English voice"
        )

    # ----------------------
    # Generate speech
    # ----------------------

    try:

        process = subprocess.Popen(
            [
                PIPER_PATH,
                "--model",
                model,
                "--output_file",
                output_file
            ],
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            text=True,
            encoding="utf-8"
        )

        process.communicate(text)

        # ----------------------
        # Play audio
        # ----------------------

        pygame.mixer.music.load(
            output_file
        )

        pygame.mixer.music.play()

        while (
            pygame.mixer.music.get_busy()
        ):
            time.sleep(0.05)

        pygame.mixer.music.stop()
        pygame.mixer.music.unload()

        time.sleep(0.1)

    except Exception as e:

        print(
            "❌ Speaker Error:",
            e
        )

    finally:

        # ----------------------
        # Delete audio file
        # ----------------------

        try:

            if os.path.exists(
                output_file
            ):

                os.remove(
                    output_file
                )

                print(
                    "🗑️ Audio deleted"
                )

        except Exception as e:

            print(
                "Delete Error:",
                e
            )