import whisper
import sounddevice as sd
import scipy.io.wavfile as wav
import numpy as np

#load the whisper model
model=whisper.load_model("medium")


def listen():
    duration=5
    sample_rate=16000

    print("🎙️ Listening...,Speak now")

    audio=sd.rec(
        int(duration*sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype="int16"
    )

    sd.wait()

    volume=np.abs(audio).mean()
    print(f"🔊 Volume: {volume}")

    if volume<20:
        return None


    audio_path="temp_audio.wav"

    wav.write(audio_path,sample_rate,audio)

    print("⏹️ Processing speech...")

    result=model.transcribe(audio_path,language="en"
    ,fp16=False,
    temperature=0)

    text=result["text"].strip()

    if text=="":
       return None 
    
    return text