from tools.command import execute_command


def route_request(text):

    text = text.lower().strip()

    print(
        f"📌 Routing text: {text}"
    )

    # -------------------
    # Force Commands
    # -------------------

    command_keywords = [

        # English
        "open",
        "launch",
        "start",
        "search",
        "find",

        # Hindi/Hinglish
        "kholo",
        "खोलो",
        "chaloo karo",
        "chalu karo",
        "चालू करो",
        "ढूंढो",
        "खोजो",

        # direct app names
        "chrome",
        "youtube",
        "google",
        "calculator",
        "settings",
        "notepad"
    ]

    is_command = any(
        keyword in text
        for keyword in command_keywords
    )

    print(
        f"⚡ Is command: {is_command}"
    )

    # -------------------
    # Execute command
    # -------------------

    if is_command:

        response = execute_command(text)

        print(
            f"⚡ Command result: {response}"
        )

        return {
            "type": "command",
            "response": response
        }

    # -------------------
    # AI Chat
    # -------------------

    return {
        "type": "chat",
        "response": None
    }