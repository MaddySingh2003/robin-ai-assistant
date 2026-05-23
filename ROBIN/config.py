from transformers import pipeline

pipe = pipeline(
    "automatic-speech-recognition",
    model="Oriserve/Whisper-Hindi2Hinglish-Prime",
    device=0
)

print("Loaded successfully")