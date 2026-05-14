from core.listener import listen 
from core.brain import ask_ai
from core.speaker import speak
from assistant.router import route_request



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

    result=route_request(text)

    if result["type"] == "command":

      if result["response"]:
         speak(result["response"])

      else:
          speak(
            "Sorry, I couldn't understand "
            "that command."
          )
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
