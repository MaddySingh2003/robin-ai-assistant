import subprocess
import os
import time
from playsound import playsound

PIPER_PATH=r"D:\AI-Assistant\piper\piper.exe"
MODEL_PATH=r"D:\AI-Assistant\piper\models\en_us-amy-medium.onnx"

OUTPUT_FILE="voice.wav"

def speak(text):

    print("ROBIN:", text)
    
    process=subprocess.Popen(
        [
            PIPER_PATH,
            "--model",
            MODEL_PATH,
            "--output_file",
            OUTPUT_FILE,
        ],
        stdin=subprocess.PIPE,
        text=True
    )

    process.communicate(text)

    playsound(OUTPUT_FILE)

    time.sleep(0.5)

    try:
        if os.path.exists(OUTPUT_FILE):
            os.remove(OUTPUT_FILE)
    
    except PermissionError:
           pass