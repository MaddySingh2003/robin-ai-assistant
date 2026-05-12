import ollama

def ask_api(prompt):
    response = ollama.chat(
        model="qwen2.5:3b",
        messages=[{
            "role": "system",
            "content":"""
            Your name is Robin, you are smart local AI assistant like Jarvis,siri,alexa.
            keep responses short, natural,and helpful.
            Talk like professional assistant.
            if someone ask your name,say your name is Robin.

"""
        },
        {
            "role": "user",
            "content": prompt
        }
        ]
 
            )
    return response["message"]["content"]