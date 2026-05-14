from faster_whisper import WhisperModel
import sounddevice as sd
import scipy.io.wavfile as wav
import numpy as np


model = WhisperModel(
    "medium",
    device="cpu",
    compute_type="int8"
)


def listen():

    duration = 5
    sample_rate = 16000

    print("🎙️ Listening..., Speak now")

    audio = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype="int16"
    )

    sd.wait()

    volume = np.abs(audio).mean()
    print(f"🔊 Volume: {volume}")

    if volume < 20:
        print("😒 no speech detected")
        return None

    audio_path = "temp_audio.wav"

    wav.write(audio_path, sample_rate, audio)

    print("⏹️ Processing speech...")

    # Only English + Hindi/Hinglish
    segments, info = model.transcribe(
        audio_path,
        beam_size=5,
        language=None,
        vad_filter=True,
        initial_prompt="""
        This assistant understands:
        English,
        Hindi,
        Hinglish.

        Example phrases:
        kya haal hai
        youtube kholo
        chrome kholo
        mujhse hinglish mein baat karo
        talk to me in hindi
        open chrome
        open youtube
        """
    )

    text = " ".join(
        segment.text for segment in segments
    ).strip()

    detected_language = info.language

    # Block weird languages
    allowed_languages = ["en", "hi"]

    if detected_language not in allowed_languages:
        print(
            f"⚠️ Unsupported language "
            f"detected: {detected_language}"
        )

        # Treat Hinglish as Hindi/English
        detected_language = "hi"

    print(
        f"🌍 Detected language: "
        f"{detected_language}"
    )

    if not text:
        return None

    return text