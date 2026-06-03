import sys
try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except AttributeError:
    pass

import tempfile
import sounddevice as sd
from scipy.io.wavfile import write
from faster_whisper import WhisperModel
from transformers import pipeline
import numpy as np
import re
import os
import torch
import time


print("Loading speech models...")


# ======================================
# DEVICE DETECTION & MODEL INITIALIZATION
# ======================================

device = "cuda" if torch.cuda.is_available() else "cpu"
compute_type = "float16" if torch.cuda.is_available() else "int8"

print(f"Device selected: {device} (compute_type: {compute_type})")

# ======================================
# FAST MODEL
# ======================================

fast_model = WhisperModel(
    "distil-large-v3",
    device=device,
    compute_type=compute_type
)


# ======================================
# HINGLISH MODEL (LAZY LOADED)
# ======================================

hinglish_model = None

def get_hinglish_model():
    global hinglish_model
    if hinglish_model is None:
        print("⏳ Lazy loading Hinglish model (first time use)...")
        hinglish_model = pipeline(
            "automatic-speech-recognition",
            model="Oriserve/Whisper-Hindi2Hinglish-Prime",
            device=0 if torch.cuda.is_available() else -1
        )
        print("🔥 Hinglish model loaded!")
    return hinglish_model

print("Speech model (distil-large-v3) loaded!")


# ======================================
# SETTINGS
# ======================================

SAMPLE_RATE = 16000
DURATION = 4
MIN_VOLUME = 10


# ======================================
# MICROPHONE
# ======================================

def get_microphone():

    print("\n🎤 Available microphones:\n")

    devices = sd.query_devices()

    best_mic = None

    for i, dev in enumerate(devices):

        if dev["max_input_channels"] > 0:

            print(f"[{i}] {dev['name']}")

            name = dev["name"].lower()

            if (
                "microphone array" in name
                or "intel" in name
                or "realtek" in name
            ):
                best_mic = i
                break

    if best_mic is None:
        best_mic = sd.default.device[0]

    print(f"\n✅ Using mic: {best_mic}")

    return best_mic


MIC_DEVICE = get_microphone()


# ======================================
# HINGLISH RETRY CHECK
# ======================================

def should_retry_hinglish(text):

    text = text.lower().strip()

    # ONLY suspicious phrases
    suspicious = [

        "python to explain",
        "go explain",
        "coeexplain",
        "eexplain",
        "a lone mask",
        "alone must",
        "lone mask",
        "who is alone",
        "athen",
        "fulllow",
    ]

    if any(
        x in text
        for x in suspicious
    ):
        return True

    # partial hinglish
    hinglish_words = {

        "kya",
        "kaise",
        "kyun",
        "hai",
        "ko",
        "kar",
        "karo",
        "samjhao",
        "batao",
        "matlab"
    }

    if any(
        word in text
        for word in hinglish_words
    ):
        return True

    return False


# ======================================
# TEXT CLEANER
# ======================================

def clean_text(text):
    replacements = {

    # explain fixes
    "co explain": "ko explain",
    "co-explain": "ko explain",
    "coexplain": "ko explain",
    "go explain": "ko explain",
    "to explain": "ko explain",

    # kholo mistakes
    "kolu": "kholo",
    "kolo": "kholo",
    "fullo": "kholo",
    "follow": "kholo",
    "openo": "open",
    "prom": "chrome",

    # whisper weirdness
    "youtube follow": "youtube kholo",
    "youtube kolu": "youtube kholo",
}

    text = text.lower().strip()

    text = re.sub(
        r"[^\w\s\u0900-\u097F]",
        "",
        text
    )

    fixes = {

        "eexplain":
        "explain",

        "explais":
        "explain",

        "explane":
        "explain",

        "python to explain":
        "python ko explain",

        "python go explain":
        "python ko explain",

        "pythonoeexplain":
        "python ko explain",

        "coeexplain":
        "ko explain",

        "kro":
        "karo",

        "a lone mask":
        "elon musk",

        "alone must":
        "elon musk",

        "lone mask":
        "elon musk",

        "vs code":
        "vscode",

        "visual studio":
        "vscode",

        "okay bye":
        "bye"
    }

    for wrong, right in fixes.items():

        text = text.replace(
            wrong,
            right
        )

    words = text.split()

    cleaned = []

    for word in words:

        if (
            not cleaned
            or cleaned[-1] != word
        ):
            cleaned.append(word)

    text = " ".join(cleaned)

    print(f"🧹 Cleaned: {text}")

    return text


# ======================================
# DELETE TEMP AUDIO
# ======================================

def delete_temp_audio(path):

    if not path:
        return

    for _ in range(10):

        try:

            if os.path.exists(path):

                os.remove(path)

                print(
                    "🗑️ Temp audio deleted"
                )

            return

        except PermissionError:

            time.sleep(0.1)


# ======================================
# LISTEN
# ======================================

def listen():

    global MIC_DEVICE

    print(
        "🎙️ Listening..., Speak now"
    )

    temp_audio_path = None

    try:

        # Record using InputStream to dynamically stop on silence
        chunk_duration = 0.1  # 100ms chunks
        chunk_size = int(SAMPLE_RATE * chunk_duration)
        silence_limit = 1.0  # 1.0 second of silence to stop
        max_duration = 8.0   # max 8 seconds total

        audio_chunks = []
        silence_chunks = 0
        speaking = False

        with sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype="float32",
            device=MIC_DEVICE
        ) as stream:

            start_time = time.time()

            while time.time() - start_time < max_duration:

                chunk, overflowed = stream.read(chunk_size)
                audio_chunks.append(chunk)

                # Calculate volume
                volume = np.nanmean(np.abs(chunk)) * 1000

                if volume > MIN_VOLUME:
                    if not speaking:
                        print("🗣️ Speaking detected...")
                        speaking = True
                    silence_chunks = 0
                else:
                    if speaking:
                        silence_chunks += 1
                        # If silence persists, stop recording
                        if silence_chunks >= (silence_limit / chunk_duration):
                            print("⏹️ Silence detected, stopping...")
                            break
                    else:
                        # Timeout if no speech is detected within 2.5 seconds
                        if time.time() - start_time > 2.5:
                            print("😒 no speech detected")
                            return None

        if not audio_chunks:
            return None

        audio = np.concatenate(audio_chunks, axis=0)

        volume = np.nanmean(np.abs(audio)) * 1000
        print(f"🔊 Volume: {volume:.2f}")

        print(
            "⏹️ Processing speech..."
        )

        with tempfile.NamedTemporaryFile(
            suffix=".wav",
            delete=False
        ) as temp_audio:

            temp_audio_path = temp_audio.name

            write(
                temp_audio_path,
                SAMPLE_RATE,
                audio
            )

        # ------------------------
        # FAST MODEL (beam_size=1 for speed on CPU)
        # ------------------------

        segments, info = (
            fast_model.transcribe(
                temp_audio_path,
                beam_size=1,
                vad_filter=True,
                language=None,
                task="transcribe",
                condition_on_previous_text=False
            )
        )

        fast_text = " ".join(
            segment.text
            for segment in segments
        ).lower().strip()

        print(
            f"🌍 Language: {info.language}"
        )

        print(
            f"⚡ Fast Model: {fast_text}"
        )

        text = fast_text

        # ------------------------
        # RETRY ONLY IF NEEDED
        # ------------------------

        if should_retry_hinglish(
            fast_text
        ):

            print(
                "🔁 Retrying with Hinglish model..."
            )

            try:

                model = get_hinglish_model()

                with torch.inference_mode():

                    result = model(
                        temp_audio_path
                    )

                better_text = (
                    result["text"]
                    .lower()
                    .strip()
                )

                print(
                    f"🔥 Hinglish Model: {better_text}"
                )

                if (
                    "kya" in better_text
                    or "ko" in better_text
                    or "hai" in better_text
                ):
                    text = better_text

            except Exception as e:

                print(
                    "❌ Hinglish model error:",
                    e
                )

        text = clean_text(text)

        if not text:
            return None

        print(
            f"📝 Heard: {text}"
        )

        return text

    except Exception as e:

        print(
            "❌ Listener error:",
            e
        )

        MIC_DEVICE = get_microphone()

        return None

    finally:

        delete_temp_audio(
            temp_audio_path
        )