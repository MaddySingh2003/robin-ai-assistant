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

    # ---------------------------------
    # Hindi script = Hindi
    # ---------------------------------

    if re.search(
        r'[\u0900-\u097F]',
        text
    ):
        return "hindi"

    # ---------------------------------
    # Hinglish detection
    # ---------------------------------

    hinglish_words = [

        "kya",
        "kaise",
        "kyun",
        "tum",
        "aap",
        "mujhe",
        "samjhao",
        "batao",
        "sakta",
        "sakti",
        "kar",
        "karo",
        "kr",
        "hai",
        "nahi",
        "ke bare me",
        "madad karti hai",
        "use hota hai",
        "coding easy banati hai",
        "python ek"
    ]

    score = sum(
        word in text
        for word in hinglish_words
    )

    # Require stronger match
    if score >= 2:
        return "hinglish"

    return "english"

# ==========================================
# SAFE DELETE AUDIO
# ==========================================

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