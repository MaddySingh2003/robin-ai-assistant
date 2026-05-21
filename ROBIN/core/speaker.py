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

    # --------------------------
    # Hindi script → Hinglish
    # --------------------------

    if re.search(
        r'[\u0900-\u097F]',
        text
    ):
        return "hinglish"

    # --------------------------
    # Hinglish words
    # --------------------------

    hinglish_words = [

        "hai",
        "ho",
        "hoo",
        "hota",
        "hoti",
        "kar",
        "karo",
        "kr",
        "ko",
        "ka",
        "ki",
        "ke",
        "ek",
        "jo",
        "kya",
        "kaise",
        "kyun",
        "tum",
        "aap",
        "mujhe",
        "mera",
        "samjhao",
        "batao",
        "banati",
        "easy banati",
        "use hota",
        "sakta",
        "sakti"
    ]

    hinglish_score = sum(
        word in text
        for word in hinglish_words
    )

    # --------------------------
    # English words
    # --------------------------

    english_words = [

        "what",
        "why",
        "where",
        "when",
        "how",
        "thank you",
        "hello",
        "goodbye",
        "anything else",
        "used for",
        "programming language",
        "development",
        "artificial intelligence",
        "readability",
        "learning"
    ]

    english_score = sum(
        word in text
        for word in english_words
    )

    # Hinglish wins
    if hinglish_score >= 2:
        return "hinglish"

    # English
    if english_score >= 1:
        return "english"

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