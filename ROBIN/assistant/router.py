from tools.command import execute_command
import re


def normalize_command(text):

    text = text.lower().strip()

    text = re.sub(
        r"[^\w\s]",
        "",
        text
    )

    # --------------------
    # Fix whisper mistakes
    # --------------------

    replacements = {

        "grom": "chrome",
        "krom": "chrome",
        "crome": "chrome",
        "rome": "chrome",
        "kohl": "chrome",
        "holon": "",
        "hollow": "",
        "web": "",
    }

    for wrong, correct in replacements.items():

        text = text.replace(
            wrong,
            correct
        )

    # --------------------
    # Auto command fixes
    # --------------------

    if "chrome" in text:

        return "open chrome"

    if "youtube" in text:

        return "open youtube"

    if "google" in text:

        return "open google"

    if "calculator" in text:

        return "open calculator"

    if "settings" in text:

        return "open settings"

    if "notepad" in text:

        return "open notepad"

    return text


def route_request(text):

    text = normalize_command(text)

    print(
        f"📌 Routing text: {text}"
    )

    command_keywords = [

        "open",
        "launch",
        "start",
        "search",
        "find",
        "chrome",
        "youtube",
        "google",
        "calculator",
        "settings",
        "notepad",
        "kholo",
        "खोलो"
    ]

    is_command = any(
        word in text
        for word in command_keywords
    )

    print(
        f"⚡ Is command: {is_command}"
    )

    if is_command:

        response = execute_command(
            text
        )

        print(
            f"⚡ Command result: "
            f"{response}"
        )

        return {
            "type": "command",
            "response": response
        }

    return {
        "type": "chat",
        "response": None
    }