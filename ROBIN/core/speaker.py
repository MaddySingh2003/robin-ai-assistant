import subprocess
import os
import time
import uuid
import pygame


PIPER_PATH = r"D:\AI-Assistant\piper\piper.exe"

ENGLISH_MODEL = (
    r"D:\AI-Assistant\piper\models\en_US-amy-medium.onnx"
)

HINDI_MODEL = (
    r"D:\AI-Assistant\piper\models\hi_IN-priyamvada-medium.onnx"
)


pygame.mixer.init()


def is_hindi(text):
    return any('\u0900' <= char <= '\u097F' for char in text)


def speak(text):

    print("ROBIN:", text)

    output_file = (
        f"voice_{uuid.uuid4().hex[:8]}.wav"
    )

    hindi_detected = is_hindi(text)

    print("Hindi detected:", hindi_detected)

    if hindi_detected:
        model = HINDI_MODEL
        print("Using Hindi voice")
    else:
        model = ENGLISH_MODEL
        print("Using English voice")

    # Generate speech
    process = subprocess.Popen(
        [
            PIPER_PATH,
            "--model",
            model,
            "--output_file",
            output_file
        ],
        stdin=subprocess.PIPE,
        text=True,
        encoding="utf-8"
    )

    process.communicate(text)

    # Play audio
    pygame.mixer.music.load(
        output_file
    )

    pygame.mixer.music.play()

    # Wait until audio finishes
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)

    # Stop and unload file
    pygame.mixer.music.stop()
    pygame.mixer.music.unload()

    # Small delay
    time.sleep(0.2)

    # Delete file
    if os.path.exists(output_file):
        os.remove(output_file)

        print("🗑️ Audio deleted")