import webbrowser
import os
import subprocess
import re


def execute_command(text):

    text = text.lower().strip()

    # ==================================
    # FIX COMMON WHISPER MISTAKES
    # ==================================

    fixes = {

        "grom": "chrome",
        "crome": "chrome",
        "krom": "chrome",

        "emd": "cmd",
        "tmd": "cmd",

        "v s code": "vs code",
        "vs-code": "vs code",

        "you tube": "youtube",

        "khol": "open",
        "kholo": "open",
        "start karo": "open",
        "chalu karo": "open",
    }

    for wrong, right in fixes.items():

        text = re.sub(
            rf"\b{wrong}\b",
            right,
            text
        )

    # ==================================
    # HINDI / HINGLISH NORMALIZATION
    # ==================================

    replacements = {

        "क्रोम": "chrome",
        "यूट्यूब": "youtube",
        "गूगल": "google",
        "सेटिंग्स": "settings",
        "कैलकुलेटर": "calculator",
        "नोटपैड": "notepad",
        "कमांड": "cmd",

        "chrome open": "open chrome",
        "youtube open": "open youtube",
        "google open": "open google",
        "calculator open": "open calculator",
        "notepad open": "open notepad",
        "cmd open": "open cmd",
        "terminal open": "open terminal",

        "chrome kholo": "open chrome",
        "youtube kholo": "open youtube",
        "google kholo": "open google",
        "calculator kholo": "open calculator",
        "settings kholo": "open settings",
        "cmd kholo": "open cmd",
        "terminal kholo": "open terminal",
        "vs code kholo": "open vs code",
        "vscode kholo": "open vs code",

        "command prompt": "cmd",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    print(f"Normalized command: {text}")

    # ==================================
    # YOUTUBE SEARCH (GENERALIZED)
    # ==================================

    if "youtube" in text and (
        "search" in text
        or "play" in text
    ):

        query = text

        remove_words = [

            "search",
            "play",
            "youtube",
            "on youtube",
            "open"
        ]

        for word in remove_words:
            query = query.replace(
                word, ""
            )

        query = query.strip()

        if query:

            webbrowser.open(
                f"https://www.youtube.com/results?search_query={query}"
            )

            return (
                f"Searching {query} on YouTube"
            )

    # ==================================
    # GOOGLE SEARCH (GENERALIZED)
    # ==================================

    if (
        "search" in text
        or text.startswith("google ")
    ):

        query = text

        remove_words = [

            "search",
            "google",
            "open"
        ]

        for word in remove_words:

            query = query.replace(
                word, ""
            )

        query = query.strip()

        if query:

            webbrowser.open(
                f"https://www.google.com/search?q={query}"
            )

            return (
                f"Searching for {query}"
            )

    # ==================================
    # OPEN APPS
    # ==================================

    if "open chrome" in text:

        try:

            os.system(
                "start chrome"
            )

            return (
                "Opening Chrome"
            )

        except:

            chrome_paths = [

                r"C:\Program Files\Google\Chrome\Application\chrome.exe",

                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",

                os.path.expandvars(
                    r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"
                )
            ]

            for path in chrome_paths:

                if os.path.exists(path):

                    subprocess.Popen(path)

                    return (
                        "Opening Chrome"
                    )

            return (
                "Chrome not found"
            )

    elif (
        "open vs code" in text
        or "open vscode" in text
    ):

        try:

            subprocess.Popen(
                "code"
            )

            return (
                "Opening VS Code"
            )

        except:

            vscode_paths = [

                r"C:\Users\Milan\AppData\Local\Programs\Microsoft VS Code\Code.exe",

                r"C:\Program Files\Microsoft VS Code\Code.exe",
            ]

            for path in vscode_paths:

                if os.path.exists(path):

                    subprocess.Popen(path)

                    return (
                        "Opening VS Code"
                    )

            return (
                "VS Code not found"
            )

    elif "open cmd" in text:

        subprocess.Popen("cmd")

        return (
            "Opening Command Prompt"
        )

    elif "open terminal" in text:

        subprocess.Popen("wt")

        return (
            "Opening Terminal"
        )

    elif "powershell" in text:

        subprocess.Popen(
            "powershell"
        )

        return (
            "Opening PowerShell"
        )

    elif "open calculator" in text:

        subprocess.Popen(
            "calc"
        )

        return (
            "Opening Calculator"
        )

    elif "open notepad" in text:

        subprocess.Popen(
            "notepad"
        )

        return (
            "Opening Notepad"
        )

    elif "open settings" in text:

        os.system(
            "start ms-settings:"
        )

        return (
            "Opening Settings"
        )

    elif "task manager" in text:

        subprocess.Popen(
            "taskmgr"
        )

        return (
            "Opening Task Manager"
        )

    elif (
        "file explorer" in text
        or "explorer" in text
    ):

        subprocess.Popen(
            "explorer"
        )

        return (
            "Opening File Explorer"
        )

    # ==================================
    # WEB APPS
    # ==================================

    elif "open youtube" in text:

        webbrowser.open(
            "https://www.youtube.com"
        )

        return (
            "Opening YouTube"
        )

    elif "open google" in text:

        webbrowser.open(
            "https://www.google.com"
        )

        return (
            "Opening Google"
        )

    elif "github" in text:

        webbrowser.open(
            "https://github.com"
        )

        return (
            "Opening GitHub"
        )

    elif "gmail" in text:

        webbrowser.open(
            "https://mail.google.com"
        )

        return (
            "Opening Gmail"
        )

    elif "chatgpt" in text:

        webbrowser.open(
            "https://chat.openai.com"
        )

        return (
            "Opening ChatGPT"
        )

    return None