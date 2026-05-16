import webbrowser
import os
import subprocess


def execute_command(text):

    text = text.lower().strip()

    # -------------------------
    # Hindi / Hinglish Mapping
    # -------------------------

    replacements = {

        "खोलो": "open",
        "खोल": "open",
        "chalu karo": "open",
        "चालू करो": "open",
        "start karo": "open",

        "यूट्यूब": "youtube",
        "क्रोम": "chrome",
        "गूगल": "google",
        "कैलकुलेटर": "calculator",
        "नोटपैड": "notepad",
        "सेटिंग्स": "settings",

        # Hinglish
        "youtube kholo": "open youtube",
        "chrome kholo": "open chrome",
        "google kholo": "open google",
        "calculator kholo": "open calculator",

        # Hindi
        "यूट्यूब खोलो": "open youtube",
        "क्रोम खोलो": "open chrome",
        "गूगल खोलो": "open google",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    print(f"Normalized command: {text}")

    # =================================
    # SEARCH YOUTUBE (FIRST PRIORITY)
    # =================================

    if "search" in text and "youtube" in text:

        query = (
            text
            .replace("search", "")
            .replace("on youtube", "")
            .replace("youtube", "")
            .strip()
        )

        if query:

            url = (
                "https://www.youtube.com/results?"
                f"search_query={query}"
            )

            webbrowser.open(url)

            return (
                f"Searching {query} on YouTube"
            )

    # =================================
    # NORMAL SEARCH
    # =================================

    elif "search" in text:

        query = (
            text
            .replace("search", "")
            .strip()
        )

        if query:
            webbrowser.open(
                f"https://www.google.com/search?q={query}"
            )

            return (
                f"Searching for {query}"
            )

        return "What should I search?"

    # =================================
    # DESKTOP APPS
    # =================================

    elif "chrome" in text:

        chrome_path = (
            r"C:\Program Files\Google"
            r"\Chrome\Application\chrome.exe"
        )

        if os.path.exists(chrome_path):
            subprocess.Popen(chrome_path)
            return "Opening Chrome"

        return "Chrome not found"

    elif "calculator" in text:
        subprocess.Popen("calc")
        return "Opening Calculator"

    elif "notepad" in text:
        subprocess.Popen("notepad")
        return "Opening Notepad"

    elif (
        "settings" in text
        or "setting" in text
    ):
        os.system("start ms-settings:")
        return "Opening Settings"

    elif (
        "command prompt" in text
        or "cmd" in text
    ):
        subprocess.Popen("cmd")
        return "Opening Command Prompt"

    elif "powershell" in text:
        subprocess.Popen("powershell")
        return "Opening PowerShell"

    elif (
        "file explorer" in text
        or "explorer" in text
    ):
        subprocess.Popen("explorer")
        return "Opening File Explorer"

    elif "task manager" in text:
        subprocess.Popen("taskmgr")
        return "Opening Task Manager"

    # =================================
    # WEB COMMANDS
    # =================================

    elif "youtube" in text:
        webbrowser.open(
            "https://www.youtube.com"
        )
        return "Opening YouTube"

    elif "google" in text:
        webbrowser.open(
            "https://www.google.com"
        )
        return "Opening Google"

    elif "github" in text:
        webbrowser.open(
            "https://github.com"
        )
        return "Opening GitHub"

    elif "gmail" in text:
        webbrowser.open(
            "https://mail.google.com"
        )
        return "Opening Gmail"

    elif "chatgpt" in text:
        webbrowser.open(
            "https://chat.openai.com"
        )
        return "Opening ChatGPT"

    return None