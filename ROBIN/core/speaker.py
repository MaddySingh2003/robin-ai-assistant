import sys
try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except AttributeError:
    pass

import subprocess
import os
import time
import uuid
import pygame
import re

from pathlib import Path

# ==========================================
# PIPER CONFIG
# ==========================================
# speaker.py -> core -> ROBIN
BASE_DIR = Path(__file__).resolve().parent.parent

PIPER_DIR = BASE_DIR / "piper"

PIPER_PATH = PIPER_DIR / "piper.exe"

ENGLISH_MODEL = PIPER_DIR / "models" / "en_US-amy-medium.onnx"

HINDI_MODEL = PIPER_DIR / "models" / "hi_IN-priyamvada-medium.onnx"


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

    # Expanded, safe Hinglish word list that doesn't conflict with common English words
    hinglish_words = {
        "hai", "kar", "karo", "ka", "ki", "ke", "ko", "ek", "kya", "kaise",
        "kyun", "aap", "tum", "mujhe", "mera", "samjhao", "batao", "sakta",
        "sakti", "hu", "aur", "toh", "tha", "thi", "raha", "rahi", "rahe",
        "hoga", "hogi", "hoge", "gaya", "gayi", "gaye", "karta", "karti",
        "karte", "diya", "liya", "kiya", "kijiye", "karke", "chalo", "achha",
        "accha", "badhiya", "theek", "batao", "samjha", "kholo", "chalu",
        "niklo", "jao", "aao", "karna", "krna"
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

    # If any Hinglish keywords are found, classify as Hinglish
    if matches >= 1:
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

def speak(text, language=None):

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

    if language is None:
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
                str(PIPER_PATH),
                "--model",
                str(model),
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