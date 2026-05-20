import tempfile
import sounddevice as sd
from scipy.io.wavfile import write
from faster_whisper import WhisperModel
import numpy as np
import re
import os


# =====================================
# MODEL
# =====================================

print("Loading speech model...")

model = WhisperModel(
    "large-v3",
    device="cuda",
    compute_type="int8_float16"
)

print("Speech model loaded!")


# =====================================
# SETTINGS
# =====================================

SAMPLE_RATE = 16000
DURATION = 5
SILENCE_THRESHOLD = 0.01


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

            # Prefer REAL laptop microphone
            if (
                "intel" in name
                or "microphone array" in name
            ):

                best_mic = i

                break

    # fallback to Windows default
    if best_mic is None:

        try:

            best_mic = (
                sd.default.device[0]
            )

        except:
            best_mic = None

    print(
        f"\n✅ Using mic: "
        f"{best_mic}"
    )

    return best_mic


MIC_DEVICE = get_microphone()


# =====================================
# CLEAN TEXT
# =====================================

def clean_text(text):

    text = text.lower().strip()

    text = text.replace(",", "")
    text = text.replace(".", "")

    replacements = {

        "hingling": "hinglish",
        "hinglis": "hinglish",
        "hingligh": "hinglish",
        "explate": "explain",
        "grom": "chrome",
        "rome": "chrome",
        "kolo": "kholo",
        "holo": "kholo",
    }

    for wrong, right in replacements.items():

        text = text.replace(
            wrong,
            right
        )

    return text


# =====================================
# DELETE AUDIO
# =====================================

def delete_temp_audio(path):

    try:

        if (
            path
            and os.path.exists(path)
        ):

            os.remove(path)

            print(
                "🗑️ Temp audio deleted"
            )

    except:
        pass


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

        audio = sd.rec(
            int(
                DURATION
                * SAMPLE_RATE
            ),
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype="float32",
            device=MIC_DEVICE
        )

        sd.wait()

        # FIX NaN volume
        volume = np.nanmean(
            np.abs(audio)
        ) * 1000

        if np.isnan(volume):
            volume = 0

        print(
            f"🔊 Volume: {volume}"
        )

        if volume < 10:

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

            temp_audio_path = (
                temp_audio.name
            )

            write(
                temp_audio_path,
                SAMPLE_RATE,
                audio
            )

        segments, info = model.transcribe(
    temp_audio.name,

    language=None,

    beam_size=8,

    best_of=5,

    temperature=0,

    task="transcribe",

    vad_filter=True,

    vad_parameters=dict(
        min_silence_duration_ms=400
    ),

    condition_on_previous_text=False
)
        text = " ".join(
            segment.text
            for segment in segments
        )

        text = clean_text(text)

        if not text:
            return None

        print(
            "🌍 Language:",
            info.language
        )

        print(
            f"📝 Heard: {text}"
        )

        return text

    except Exception as e:

        print(
            "❌ Listener error:",
            e
        )

        # auto mic recovery
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