from core.listener import listen 


print("ROBIN: Hello! I'm ROBIN, your AI assistant.")
print("Speak after the microphone starts")



while True:
    text = listen()

    print("You said:", text)