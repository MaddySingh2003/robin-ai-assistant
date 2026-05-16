import webbrowser
import os
import subprocess


def execute_command(text):

    text = text.lower().strip()

    # ==========================
    # SMART SHORTCUTS
    # ==========================

    shortcuts = {

        "chrome": "open chrome",
        "youtube": "open youtube",
        "google": "open google",
        "settings": "open settings",
        "calculator": "open calculator",
        "notepad": "open notepad",
        "cmd": "open cmd",
        "terminal": "open terminal",
    }

    if text in shortcuts:
        text = shortcuts[text]

    # ==========================
    # HINDI / HINGLISH SUPPORT
    # ==========================

    replacements = {

        # Open
        "खोलो": "open",
        "खोल": "open",
        "kholo": "open",
        "chalu karo": "open",
        "start karo": "open",

        # Apps
        "क्रोम": "chrome",
        "यूट्यूब": "youtube",
        "गूगल": "google",
        "सेटिंग्स": "settings",
        "कैलकुलेटर": "calculator",
        "नोटपैड": "notepad",
        "कमांड": "cmd",

        # Hinglish
        "chrome kholo": "open chrome",
        "youtube kholo": "open youtube",
        "google kholo": "open google",
        "settings kholo": "open settings",
        "calculator kholo": "open calculator",
        "cmd kholo": "open cmd",
        "terminal kholo": "open terminal",

        # Hindi
        "क्रोम खोलो": "open chrome",
        "यूट्यूब खोलो": "open youtube",
        "गूगल खोलो": "open google",
        "सेटिंग्स खोलो": "open settings",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    print(f"Normalized command: {text}")

    # ==========================
    # YOUTUBE SEARCH
    # ==========================

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

    # ==========================
    # GOOGLE SEARCH
    # ==========================

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

    # ==========================
    # DESKTOP APPS
    # ==========================

    elif "open chrome" in text:

        chrome_paths = [

            r"C:\Program Files\Google\Chrome\Application\chrome.exe",

            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        ]

        for path in chrome_paths:

            if os.path.exists(path):
                subprocess.Popen(path)
                return "Opening Chrome"

        return "Chrome not found"

    elif "open cmd" in text:

        subprocess.Popen("cmd")
        return "Opening Command Prompt"

    elif "open terminal" in text:

        subprocess.Popen("wt")
        return "Opening Terminal"

    elif "open calculator" in text:

        subprocess.Popen("calc")
        return "Opening Calculator"

    elif "open notepad" in text:

        subprocess.Popen("notepad")
        return "Opening Notepad"

    elif "open settings" in text:

        os.system("start ms-settings:")
        return "Opening Settings"

    elif "powershell" in text:

        subprocess.Popen("powershell")
        return "Opening PowerShell"

    elif "task manager" in text:

        subprocess.Popen("taskmgr")
        return "Opening Task Manager"

    elif (
        "file explorer" in text
        or "explorer" in text
    ):

        subprocess.Popen("explorer")
        return "Opening File Explorer"

    # ==========================
    # WEB COMMANDS
    # ==========================

    elif "open youtube" in text:

        webbrowser.open(
            "https://www.youtube.com"
        )
        return "Opening YouTube"

    elif "open google" in text:

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