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

    text_lower = text.lower().strip()

    # Hindi script detection
    if re.search(r'[\u0900-\u097F]', text):
        return "hindi"

    # Strong Hinglish detection
    hinglish_words = [

        "samjhao",
        "samjho",
        "kaise",
        "kya",
        "kyun",
        "nahi",
        "haan",
        "mera",
        "tum",
        "aap",
        "karna",
        "batao",
        "hinglish",
        "hindi me",
        "hindi mein",
        "in hinglish"
    ]

    # only if multiple hinglish words exist
    matches = sum(
        word in text_lower
        for word in hinglish_words
    )

    if matches >= 2:
        return "hinglish"

    return "english"

# ==========================
# SAFE DELETE
# ==========================

def delete_audio(file_path):

    for _ in range(10):

        try:

            if (
                file_path
                and os.path.exists(
                    file_path
                )
            ):

                os.remove(
                    file_path
                )

                print(
                    "🗑️ Audio deleted"
                )

            return

        except PermissionError:

            time.sleep(0.2)

        except Exception as e:

            print(
                "Delete Error:",
                e
            )

            return


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

    if language in [
        "hindi",
        "hinglish"
    ]:

        # Hindi voice sounds better
        # for Hinglish also
        model = HINDI_MODEL

        print(
            "Using Hindi voice"
        )

    else:

        model = ENGLISH_MODEL

        print(
            "Using English voice"
        )

    try:

        # ----------------------
        # Generate speech
        # ----------------------

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

        # IMPORTANT FIX
        pygame.mixer.music.stop()

        try:
            pygame.mixer.music.unload()
        except:
            pass

        time.sleep(0.3)

    except Exception as e:

        print(
            "❌ Speaker Error:",
            e
        )

    finally:

        # Always delete
        delete_audio(
            output_file
        )