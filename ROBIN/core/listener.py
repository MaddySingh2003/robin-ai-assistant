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
# FAST MODEL
# ======================================

fast_model = WhisperModel(
    "distil-large-v3",
    device="cuda",
    compute_type="int8_float16"
)


# ======================================
# HINGLISH MODEL
# ======================================

hinglish_model = pipeline(
    "automatic-speech-recognition",
    model="Oriserve/Whisper-Hindi2Hinglish-Prime",
    device=0 if torch.cuda.is_available() else -1
)

print("Speech models loaded!")


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

        audio = sd.rec(
            int(SAMPLE_RATE * DURATION),
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype="float32",
            device=MIC_DEVICE
        )

        sd.wait()

        volume = (
            np.nanmean(
                np.abs(audio)
            ) * 1000
        )

        print(f"🔊 Volume: {volume}")

        if volume < MIN_VOLUME:

            print(
                "😒 no speech detected"
            )

            return None

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
        # FAST MODEL
        # ------------------------

        segments, info = (
            fast_model.transcribe(
                temp_audio_path,
                beam_size=5,
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

                result = hinglish_model(
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