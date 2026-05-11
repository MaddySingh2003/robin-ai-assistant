from core.brain import ask_api


print("ROBIN: Hello! I'm ROBIN, your AI assistant." )
print("type 'exit' to quit\n.")


while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        print("ROBIN: Goodbye!")
        break

    response = ask_api(user_input)
    print("ROBIN:",response )