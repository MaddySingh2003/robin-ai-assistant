import webbrowser
import os
import subprocess


def execute_command(text):

    text = text.lower().strip()

    # ----------------------
    # Web Commands
    # ----------------------

    if "open youtube" in text:
        webbrowser.open("https://www.youtube.com")
        return "Opening YouTube"

    elif "open google" in text:
        webbrowser.open("https://www.google.com")
        return "Opening Google"

    elif "open github" in text:
        webbrowser.open("https://github.com")
        return "Opening GitHub"

    elif "open gmail" in text:
        webbrowser.open("https://mail.google.com")
        return "Opening Gmail"

    elif "open chatgpt" in text:
        webbrowser.open("https://chat.openai.com")
        return "Opening ChatGPT"

    elif "search" in text:
        query = text.replace("search", "").strip()

        if query:
            webbrowser.open(
                f"https://www.google.com/search?q={query}"
            )
            return f"Searching for {query}"

    # ----------------------
    # Open Desktop Apps
    # ----------------------

    elif "open chrome" in text:
        os.startfile(
            "C:/Program Files/Google/Chrome/Application/chrome.exe"
        )
        return "Opening Chrome"

    elif "open notepad" in text:
        subprocess.Popen("notepad")
        return "Opening Notepad"

    elif "open calculator" in text:
        subprocess.Popen("calc")
        return "Opening Calculator"

    elif "open command prompt" in text or "open cmd" in text:
        subprocess.Popen("cmd")
        return "Opening Command Prompt"

    elif "open powershell" in text:
        subprocess.Popen("powershell")
        return "Opening PowerShell"

    elif "open file explorer" in text:
        subprocess.Popen("explorer")
        return "Opening File Explorer"

    elif "open task manager" in text:
        subprocess.Popen("taskmgr")
        return "Opening Task Manager"

    elif "open control panel" in text:
        subprocess.Popen("control")
        return "Opening Control Panel"

    elif "open settings" in text:
        os.system("start ms-settings:")
        return "Opening Settings"

    # ----------------------
    # Media / Music
    # ----------------------

    elif "play music" in text:
        music_folder = os.path.expanduser("~/Music")
        os.startfile(music_folder)
        return "Opening your music folder"

    # ----------------------
    # System Commands
    # ----------------------

    elif "lock computer" in text or "lock pc" in text:
        os.system("rundll32.exe user32.dll,LockWorkStation")
        return "Locking computer"

    elif "shutdown pc" in text:
        os.system("shutdown /s /t 10")
        return "Shutting down in 10 seconds"

    elif "restart pc" in text:
        os.system("shutdown /r /t 10")
        return "Restarting in 10 seconds"

    elif "cancel shutdown" in text:
        os.system("shutdown /a")
        return "Shutdown cancelled"

    # ----------------------
    # Folder Commands
    # ----------------------

    elif "open downloads" in text:
        os.startfile(os.path.expanduser("~/Downloads"))
        return "Opening Downloads"

    elif "open documents" in text:
        os.startfile(os.path.expanduser("~/Documents"))
        return "Opening Documents"

    elif "open desktop" in text:
        os.startfile(os.path.expanduser("~/Desktop"))
        return "Opening Desktop"

    elif "open pictures" in text:
        os.startfile(os.path.expanduser("~/Pictures"))
        return "Opening Pictures"

    # ----------------------
    # AI Project Shortcuts
    # ----------------------

    elif "open vs code" in text:
        subprocess.Popen("code")
        return "Opening Visual Studio Code"

    elif "open terminal" in text:
        subprocess.Popen("wt")
        return "Opening Terminal"

    # ----------------------
    # Fallback
    # ----------------------

    return None