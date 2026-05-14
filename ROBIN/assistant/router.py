from tools.command import execute_command


def route_request(text):

    text = text.lower().strip()

    # English command words
    open_keywords = [
        "open",
        "launch",
        "start",
        "search",
        "find"
    ]

    # Hindi / Hinglish command words
    hindi_keywords = [
        "kholo",
        "खोलो",
        "chalu karo",
        "चालू करो",
        "search karo",
        "ढूंढो",
        "खोजो"
    ]

    all_keywords = (
        open_keywords +
        hindi_keywords
    )

    # Check if command-like sentence
    if any(
        keyword in text
        for keyword in all_keywords
    ):

        command_result = execute_command(text)

        if command_result:
            return {
                "type": "command",
                "response": command_result
            }

    # Normal AI chat
    return {
        "type": "chat"
    }