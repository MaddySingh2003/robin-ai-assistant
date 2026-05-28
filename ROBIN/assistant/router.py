import re
from tools.command import execute_command




def route_request(text):

    
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