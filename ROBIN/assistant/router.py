import re
from tools.command import execute_command


def normalize_command(text):

    text = text.lower().strip()

    text = re.sub(
        r"[^\w\s]",
        "",
        text
    )

    # ==========================
    # Whisper fixes
    # ==========================

    replacements = {

        "grom": "chrome",
        "krom": "chrome",
        "crome": "chrome",

        "you tube": "youtube",
        "u tube": "youtube",

        "v s code": "vs code",
        "vs-code": "vs code",

        "khol": "open",
        "kholo": "open",

        "start karo": "open",
        "chalu karo": "open",
    }

    for wrong, right in replacements.items():

        text = text.replace(
            wrong,
            right
        )

    # ==========================
    # KEEP SEARCH TEXT SAFE
    # ==========================

    search_patterns = [

        "search",
        "play",
        "find",
        "look up",
        "in youtube",
        "on youtube",
    ]

    if any(
        x in text
        for x in search_patterns
    ):
        return text

    # ==========================
    # ONLY EXACT SHORTCUTS
    # ==========================

    shortcuts = {

        "chrome": "open chrome",
        "youtube": "open youtube",
        "google": "open google",
        "calculator": "open calculator",
        "settings": "open settings",
        "notepad": "open notepad",
        "cmd": "open cmd",
        "terminal": "open terminal",
        "powershell": "open powershell",
        "task manager": "open task manager",
        "explorer": "open explorer",
        "vs code": "open vscode",
        "vscode": "open vscode",
    }

    # IMPORTANT:
    # ONLY exact match
    if text in shortcuts:
        return shortcuts[text]

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
        "play",
        "find",

        "youtube",
        "google",
        "chrome",
        "vscode",
        "calculator",
        "settings",
        "notepad",
        "cmd",
        "terminal",
        "powershell",
        "task manager",
        "explorer",

        "shutdown",
        "restart",
        "mute",
        "volume",
    ]

    is_command = any(
        keyword in text
        for keyword in command_keywords
    )

    print(
        f"⚡ Is command: {is_command}"
    )

    if is_command:

        response = execute_command(
            text
        )

        print(
            f"⚡ Command result: {response}"
        )

        return {
            "type": "command",
            "response": response
        }

    return {
        "type": "chat",
        "response": None
    }