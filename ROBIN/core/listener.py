from faster_whisper import WhisperModel
import sounddevice as sd
import scipy.io.wavfile as wav
import numpy as np
import os
import re


# Better model for Hinglish
model = WhisperModel(
    "small",
    device="cpu",
    compute_type="int8"
)


def clean_text(text):

    text = text.lower().strip()

    # Remove weird symbols
    text = re.sub(
        r"[^\w\s]",
        "",
        text
    )

    # Remove repeated nonsense
    banned = [
        "ឡ",
        "arespace",
        "disciplinary",
        "indeer",
        "chromos",
        "mom",
        "ipedia"
    ]

    for word in banned:
        text = text.replace(word, "")

    text = " ".join(text.split())

    return text


def listen():

    duration = 7  # increased
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

    if volume < 10:
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

        segments, info = model.transcribe(
            audio_path,

            # Better accuracy
            beam_size=8,
            best_of=5,

            vad_filter=True,
            temperature=0,
            condition_on_previous_text=False,

            # Hinglish focused
            language="hi",

            initial_prompt="""
            This assistant understands:
            English
            Hindi
            Hinglish

            Example phrases:

            kya haal hai
            kaise ho
            youtube kholo
            chrome kholo
            open chrome
            open youtube
            search python tutorial on youtube
            search AI tutorial
            calculator kholo
            settings kholo
            """
        )

        text = " ".join(
            segment.text
            for segment in segments
        ).strip()
        # Common Whisper mistakes

        corrections = {

    "pane chrome": "open chrome",
    "pain chrome": "open chrome",
    "payne chrome": "open chrome",

    "hallow": "hello",
    "halu": "hello",
    "haaloo": "hello",

    "rabin": "robin",
    "robbin": "robin",

    "kha haal hai": "kya haal hai",
    "haal hai": "kya haal hai",
}

        text = text.lower().strip()

        for wrong, correct in corrections.items():
           if wrong in text:
            text = text.replace(
            wrong,
            correct
        )

        text = clean_text(text)

        if len(text) < 2:
            return None

        print(
            "🌍 Language: Hindi/Hinglish"
        )

        print(
            f"📝 Heard: {text}"
        )

        return text

    except Exception as e:
        print(
            f"❌ Error: {e}"
        )
        return None

    finally:

        if os.path.exists(audio_path):
            try:
                os.remove(audio_path)
            except:
                pass