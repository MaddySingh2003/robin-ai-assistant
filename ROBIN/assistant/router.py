import sys
try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except AttributeError:
    pass

import re
from tools.command import execute_command


# ======================================
# NORMALIZE TEXT
# ======================================

def normalize_command(text):

    text = text.lower().strip()

    text = re.sub(
        r"[^\w\s]",
        "",
        text
    )

    replacements = {

        # whisper fixes
        "grom": "chrome",
        "crome": "chrome",
        "krom": "chrome",

        "you tube": "youtube",
        "u tube": "youtube",

        "v s code": "vscode",
        "vs code": "vscode",

        "khol": "open",
        "kholo": "open",

        "start karo": "open",
        "chalu karo": "open",
    }

    for wrong, correct in replacements.items():
        text = text.replace(
            wrong,
            correct
        )

    return text


# ======================================
# COMMAND INTENT
# ======================================

def detect_command_intent(text):

    text = text.lower()

    # -----------------------------
    # actions
    # -----------------------------

    action_words = {

        "open",
        "launch",
        "start",
        "run",

        "search",
        "find",
        "play",

        "create",
        "make",
        "generate",
        "build",

        "shutdown",
        "restart",
        "mute",
        "unmute",

        "increase",
        "decrease",
    }

    # -----------------------------
    # targets
    # -----------------------------

    known_targets = {

        "chrome",
        "youtube",
        "google",
        "spotify",
        "discord",
        "telegram",
        "steam",

        "vscode",
        "notepad",
        "calculator",
        "cmd",
        "terminal",
        "powershell",
        "explorer",

        "python",
        "file",
        "folder",

        "volume",
        "brightness",
     
    "react",
    "node",
    "fast api",
    "api",
    "angular",

    "python",
    "java",
    "cpp",
    "c",

    "project",
    

    "vscode",
    "notepad",

"nextjs",
"next",
"django",
"flask",
"mern",
    }

    words = set(text.split())

    has_action = bool(
        words.intersection(
            action_words
        )
    )

    has_target = bool(
        words.intersection(
            known_targets
        )
    )

    # command confidence
    if has_action and has_target:
        return True

    # direct target mention
    if has_target and len(words) <= 5:
        return True

    return False


# ======================================
# ROUTER
# ======================================

def route_request(text):

    text = normalize_command(text)

    print(
        f"📌 Routing text: {text}"
    )

    is_command = detect_command_intent(
        text
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

        # Only route as command if a matching command was actually executed
        if response is not None:
            return {
                "type": "command",
                "response": response
            }

    return {
        "type": "chat",
        "response": None
    }