from faster_whisper import WhisperModel
import sounddevice as sd
import scipy.io.wavfile as wav
import numpy as np
import os


# Better model for Hinglish
model = WhisperModel(
    "small",
    device="cpu",
    compute_type="int8"
)


def listen():

    duration = 4
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

    # Lower threshold
    if volume < 5:
        print("😒 no speech detected")
        return None

    audio_path = "temp_audio.wav"

    wav.write(
        audio_path,
        sample_rate,
        audio
    )

    print("⏹️ Processing speech...")

    try:

        # Force Hindi/English only
        segments, info = model.transcribe(
            audio_path,
            beam_size=2,
            best_of=2,
            vad_filter=True,
            language="hi",   # Hinglish works better
            temperature=0.0,

            initial_prompt="""
            This assistant understands only:
            English, Hindi, Hinglish

            Example commands:

            chrome kholo
            youtube kholo
            open chrome
            open youtube
            kya haal hai
            kaise ho
            search AI tutorial
            calculator kholo
            google kholo
            """
        )

        text = " ".join(
            segment.text
            for segment in segments
        ).strip()

        text = text.lower()

        # Clean weird outputs
        bad_words = [
            "arespace",
            "disciplinary",
            "indeer",
            "chromos",
            "mom",
            "ipedia"
        ]

        for word in bad_words:
            text = text.replace(
                word,
                ""
            )

        text = " ".join(text.split())

        if not text:
            return None

        print(
            "🌍 Language: Hindi/Hinglish"
        )

        print("📝 Heard:", text)

        return text

    except Exception as e:
        print(
            f"❌ Speech error: {e}"
        )
        return None

    finally:
        if os.path.exists(audio_path):
            os.remove(audio_path)