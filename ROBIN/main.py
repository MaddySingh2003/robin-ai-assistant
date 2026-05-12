from core.listener import listen 
from core.brain import ask_api



print("ROBIN: Hello! I'm ROBIN, your AI assistant.")
print("Say 'exit' to quit")
print()


while True:
    text=listen()

    print("You:",text)
    
    if text.lower() == "exit":
        print("ROBIN: Goodbye!")
        break

    response=ask_api(text)
    
    print("ROBIN:",response)
