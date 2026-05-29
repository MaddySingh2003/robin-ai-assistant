import subprocess
import os
import time
import uuid
import pygame
import re


# ==========================================
# PIPER CONFIG
# ==========================================

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


# ==========================================
# INIT PYGAME
# ==========================================

pygame.mixer.init(
    frequency=22050,
    size=-16,
    channels=2,
    buffer=512
)


# ==========================================
# DETECT LANGUAGE
# ==========================================

def detect_language(text):

    text = text.lower().strip()

    # Hindi script
    if re.search(r'[\u0900-\u097F]', text):
        return "hinglish"

    hinglish_words = {

        "hai",
        "kar",
        "karo",
        "ka",
        "ki",
        "ke",
        "ko",
        "ek",
        "kya",
        "kaise",
        "kyun",
        "aap",
        "tum",
        "mujhe",
        "mera",
        "samjhao",
        "batao",
        "sakta",
        "sakti"
    }

    words = set(
        re.findall(
            r"\b\w+\b",
            text
        )
    )

    matches = len(
        words.intersection(
            hinglish_words
        )
    )

    # stricter detection
    if matches >= 3:
        return "hinglish"

    return "english"

def delete_audio(file_path):

    if not file_path:
        return

    # Windows file lock fix
    for _ in range(15):

        try:

            if os.path.exists(
                file_path
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


# ==========================================
# SPEAK
# ==========================================

def speak(text):

    if not text:
        return

    text = str(text).strip()

    print(
        "ROBIN:",
        text
    )

    output_file = (
        f"voice_"
        f"{uuid.uuid4().hex[:8]}"
        f".wav"
    )

    # --------------------------------------
    # Detect language
    # --------------------------------------

    language = detect_language(
        text
    )

    print(
        f"Detected language: "
        f"{language}"
    )

    # --------------------------------------
    # Select voice model
    # --------------------------------------

    if language in [
        "hindi",
        "hinglish"
    ]:

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

        # --------------------------------------
        # Generate speech
        # --------------------------------------

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

        process.communicate(
            text
        )

        # --------------------------------------
        # Play audio
        # --------------------------------------

        pygame.mixer.music.load(
            output_file
        )

        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():

            time.sleep(0.05)

        # --------------------------------------
        # Proper cleanup
        # --------------------------------------

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

        delete_audio(
            output_file
        )