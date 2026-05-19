import tempfile
import sounddevice as sd
from scipy.io.wavfile import write
from faster_whisper import WhisperModel
import numpy as np
import re


# =====================================
# MODEL
# =====================================

print("Loading speech model...")

model = WhisperModel(
    "distil-large-v3",
    device="cuda",   # safer first
    compute_type="int8"
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

    valid_mics = []

    for i, dev in enumerate(devices):

        if dev["max_input_channels"] > 0:

            print(f"[{i}] {dev['name']}")

            valid_mics.append(i)

    # Use Windows default input mic
    try:
        default_input = sd.default.device[0]

        if default_input in valid_mics:

            print(
                f"\n✅ Using default mic: "
                f"{default_input}"
            )

            return default_input

    except:
        pass

    # fallback
    print(
        f"\n✅ Fallback mic: "
        f"{valid_mics[0]}"
    )

    return valid_mics[0]


MIC_DEVICE = get_microphone()


# =====================================
# CLEAN TEXT
# =====================================

def clean_text(text):

    text = text.lower().strip()

    garbage_patterns = [

        r"(hoot){4,}",
        r"(itut){3,}",
        r"(.)\1{15,}",
    ]

    for pattern in garbage_patterns:

        if re.search(pattern, text):
            return ""

    return text


# =====================================
# LISTEN
# =====================================

def listen():

    print(
        "🎙️ Listening..., Speak now"
    )

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

        volume = (
            np.abs(audio).mean()
            * 1000
        )

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

            write(
                temp_audio.name,
                SAMPLE_RATE,
                audio
            )

            segments, info = model.transcribe(
                temp_audio.name,
                beam_size=3,
                vad_filter=True
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

        return None