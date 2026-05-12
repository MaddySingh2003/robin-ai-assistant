import whisper
import sounddevice as sd
import scipy.io.wavfile as wav


#load the whisper model
model=whisper.load_model("small")


def listen():
    duration=6
    sample_rate=16000

    print("🎙️ Listening...,Speak now")

    audio=sd.rec(
        int(duration*sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype="int16"
    )

    sd.wait()
    audio_path="temp_audio.wav"

    wav.write(audio_path,sample_rate,audio)
    print("⏹️ Processing speech...")
    result=model.transcribe(audio_path,language="en")
    text=result["text"]
    return text.strip()