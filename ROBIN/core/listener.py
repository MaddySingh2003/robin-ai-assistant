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
    "distil-large-v3",
    device="cuda",
    compute_type="int8_float16"
)

print("Speech model loaded!")


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

            print(
                f"[{i}] {dev['name']}"
            )

            name = dev[
                "name"
            ].lower()

            # Prefer laptop mic
            if (
                "microphone array"
                in name
                or "intel" in name
                or "realtek"
                in name
            ):

                best_mic = i
                break

    # fallback
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

    text = (
        text.lower()
        .strip()
    )

    text = re.sub(
        r"[^\w\s\u0900-\u097F]",
        "",
        text
    )

    # ---------------------------------
    # Common speech mistakes
    # ---------------------------------

    replacements = {

    # Python fixes
    "pythin": "python",
    "pythin": "python",
    "wyton": "python",
    "wythin": "python",
    "pythons": "python",
    "paython": "python",
    "pithon": "python",

    # explain fixes
    "eexplain": "explain",
    "xplain": "explain",
    "explane": "explain",
    "explan": "explain",

    # Hindi/Hinglish fixes
    "python to explain": "python ko explain",
    "python to eexplain": "python ko explain",
    "python explain": "python ko explain",
    "python explained": "python ko explain",
    "python ko eexplain": "python ko explain",

    "explainkr": "explain kar",
    "explain kro": "explain karo",
}
    for wrong, right in replacements.items():

        text = text.replace(
            wrong,
            right
        )

    # remove repeated spaces
    text = re.sub(
        r"\s+",
        " ",
        text
    )

    print(
        f"🧹 Cleaned: {text}"
    )

    return text


# =====================================
# DELETE AUDIO
# =====================================

def delete_temp_audio(path):

    if not path:
        return

    for _ in range(10):

        try:

            if os.path.exists(
                path
            ):

                os.remove(path)

                print(
                    "🗑️ Temp audio deleted"
                )

            return

        except PermissionError:

            import time
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

        # ---------------------------------
        # Record Audio
        # ---------------------------------

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

        # ---------------------------------
        # Fix NaN volume
        # ---------------------------------

        volume = (
            np.nanmean(
                np.abs(audio)
            ) * 1000
        )

        if np.isnan(volume):
            volume = 0

        print(
            f"🔊 Volume: "
            f"{volume}"
        )

        # ---------------------------------
        # Silence detect
        # ---------------------------------

        if volume < MIN_VOLUME:

            print(
                "😒 no speech detected"
            )

            return None

        print(
            "⏹️ Processing speech..."
        )

        # ---------------------------------
        # Save temp audio
        # ---------------------------------

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

        # ---------------------------------
        # Faster Whisper
        # ---------------------------------

        segments, info = model.transcribe(
    temp_audio.name,

    # AUTO DETECT
    language=None,

    task="transcribe",

    beam_size=5,
    best_of=3,

    temperature=0,

    vad_filter=True,

    vad_parameters=dict(
        min_silence_duration_ms=300
    ),
    hallucination_silence_threshold=1,

    condition_on_previous_text=False,

    # FASTER + BETTER FOR HINGLISH
    multilingual=True
)
        text = " ".join(

            segment.text
            for segment
            in segments
        )
        fixes = {

    # python mistakes
    "pythin": "python",
    "pythin": "python",
    "wyton": "python",
    "wythin": "python",
    "python's": "python",
    "ayythan": "python",

    # explain mistakes
    "eexplain": "explain",
    "explais": "explain",
    "explate": "explain",
    "explainkr": "explain kar",
    "explain kro": "explain karo",
    "corro": "karo",

    # hinglish
    "cant you": "can you",
    "coeexplain": "ko explain",
}

        text = text.lower()

        for wrong, right in fixes.items():
         text = text.replace(
        wrong,
        right
    )

# remove duplicate words
        words = text.split()

        cleaned_words = []

        for word in words:

           if (
        len(cleaned_words) == 0
        or cleaned_words[-1] != word
    ):
             cleaned_words.append(word)

        text = " ".join(cleaned_words)

        text = clean_text(text)

        if not text:
            return None

        print(
            "🌍 Language:",
            info.language
        )

        print(
            f"📝 Heard: "
            f"{text}"
        )

        return text

    except Exception as e:

        print(
            "❌ Listener error:",
            e
        )

        # Auto recover mic
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