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


# =====================================
# MODELS
# =====================================

print("Loading speech models...")


# FAST MODEL
fast_model = WhisperModel(
    "distil-large-v3",
    device="cuda",
    compute_type="int8_float16"
)


# HINGLISH FALLBACK MODEL
hinglish_model = pipeline(
    "automatic-speech-recognition",
    model="Oriserve/Whisper-Hindi2Hinglish-Prime",
    device=0 if torch.cuda.is_available() else -1
)

print("Speech models loaded!")


# =====================================
# SETTINGS
# =====================================

SAMPLE_RATE = 16000
DURATION = 4
MIN_VOLUME = 10


# =====================================
# AUTO MIC DETECT
# =====================================

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

        try:
            best_mic = sd.default.device[0]
        except:
            best_mic = None

    print(f"\n✅ Using mic: {best_mic}")

    return best_mic


MIC_DEVICE = get_microphone()


# =====================================
# BAD TRANSCRIPT DETECTOR
# =====================================

def should_retry_hinglish(text, detected_lang):

    text = text.lower().strip()
    words = text.split()

    # obvious gibberish patterns
    gibberish_patterns = [

        "whattham",
        "whython",
        "wythin",
        "athen",
        "brumco",
        "fulllow",
        "coeexplain",
        "eexplain",
        "wyton",
        "brocol",
        "burton yeah"
    ]

    if any(
        x in text
        for x in gibberish_patterns
    ):
        return True

    # Hindi wrongly detected
    if detected_lang == "hi":
        return True

    # weird repeated words
    if len(words) >= 2:

        repeated_ratio = (
            len(words)
            - len(set(words))
        ) / max(len(words), 1)

        if repeated_ratio > 0.45:
            return True

    # suspicious word quality
    weird_words = 0

    for word in words:

        # random broken word
        if (
            len(word) > 7
            and not re.match(
                r"^[a-zA-Z]+$",
                word
            )
        ):
            weird_words += 1

    if weird_words >= 1:
        return True

    # suspicious very short nonsense
    if (
        len(words) <= 3
        and any(
            len(w) > 10
            for w in words
        )
    ):
        return True

    return False


# =====================================
# TEXT CLEANER
# =====================================

def clean_text(text):

    text = text.lower().strip()

    text = re.sub(
        r"[^\w\s\u0900-\u097F]",
        "",
        text
    )

    fixes = {

        # common whisper mistakes
        "cant you": "can you",
        "dont you": "don't you",

        # explain
        "eexplain": "explain",
        "xplain": "explain",
        "explais": "explain",
        "explane": "explain",

        # broken hinglish
        "coeexplain": "ko explain",
        "corro": "karo",
        "kro": "karo",

        # coding words
        "vs code": "vscode",
        "visual studio": "vscode",

        # speech mistakes
        "okay bye": "bye",
        "bye okay": "bye",
    }

    for wrong, right in fixes.items():

        text = text.replace(
            wrong,
            right
        )

    # remove repeated words

    words = text.split()

    cleaned = []

    for word in words:

        if (
            not cleaned
            or cleaned[-1] != word
        ):
            cleaned.append(word)

    text = " ".join(cleaned)

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    print(f"🧹 Cleaned: {text}")

    return text


# =====================================
# DELETE TEMP AUDIO
# =====================================

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

        except:
            return


# =====================================
# LISTEN
# =====================================

def listen():

    global MIC_DEVICE

    print(
        "🎙️ Listening..., Speak now"
    )

    temp_audio_path = None

    try:

        # RECORD AUDIO
        audio = sd.rec(
            int(
                SAMPLE_RATE
                * DURATION
            ),
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

        if np.isnan(volume):
            volume = 0

        print(
            f"🔊 Volume: {volume}"
        )

        if volume < MIN_VOLUME:

            print(
                "😒 no speech detected"
            )

            return None

        print(
            "⏹️ Processing speech..."
        )

        # SAVE AUDIO
        with tempfile.NamedTemporaryFile(
            suffix=".wav",
            delete=False
        ) as temp_audio:

            temp_audio_path = (
                temp_audio.name
            )

            write(
                temp_audio_path,
                SAMPLE_RATE,
                audio
            )

        # =================================
        # FAST MODEL
        # =================================

        segments, info = (
            fast_model.transcribe(
                temp_audio_path,
                language=None,
                task="transcribe",
                beam_size=5,
                best_of=3,
                temperature=0,
                vad_filter=True,
                vad_parameters=dict(
                    min_silence_duration_ms=300
                ),
                condition_on_previous_text=False
            )
        )

        fast_text = " ".join(
            segment.text
            for segment in segments
        ).lower()

        print(
            f"🌍 Language: {info.language}"
        )

        print(
            f"⚡ Fast Model: {fast_text}"
        )

        text = fast_text

        # =================================
        # SMART RETRY
        # =================================

        if should_retry_hinglish(
            fast_text,
            info.language
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

                if better_text:

                    print(
                        f"🔥 Hinglish Model: {better_text}"
                    )

                    # Use better result only
                    if len(
                        better_text.split()
                    ) >= len(
                        fast_text.split()
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

        print(
            "🔄 Re-detecting microphone..."
        )

        MIC_DEVICE = (
            get_microphone()
        )

        return None

    finally:

        delete_temp_audio(
            temp_audio_path
        )