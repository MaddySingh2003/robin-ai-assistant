from core.listener import listen 
from core.brain import ask_api
from core.speaker import speak



print("ROBIN: Hello! I'm ROBIN, your AI assistant.")
print("Say 'exit' to quit\n")


try:

  while True:
    text=listen()

    if not text:
        print("😒 no speech detected")
        continue

    print("You:",text)
    
    if text.lower() == "exit":
        print("ROBIN: Goodbye!")
        break

    response=ask_api(text)
    
    speak(response)

except KeyboardInterrupt:
    print("\nROBIN: Shutting down. Goodbye!")
