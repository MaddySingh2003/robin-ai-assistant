from core.listener import listen 
from core.brain import ask_ai
from core.speaker import speak
from assistant.router import router_command



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

    result=router_command(text)

    if result["type"]=="command":
       speak(result["response"])
    else:
         # Force Hindi response if requested
        if "hindi" in text.lower():
           text = (
               f"Answer only in Hindi: {text}"
                )

        response = ask_ai(text)

        speak(response)

except KeyboardInterrupt:
    print("\nROBIN: Shutting down. Goodbye!")
