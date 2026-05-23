import webbrowser
import os
import subprocess
import re


# ======================================
# APP PATHS
# ======================================

APP_PATHS = {

    "chrome": "start chrome",

    "vscode": "code",

    "notepad": "notepad",

    "calculator": "calc",

    "cmd": "cmd",

    "terminal": "wt",

    "powershell": "powershell",

    "task manager": "taskmgr",

    "explorer": "explorer",

    "spotify": os.path.expandvars(
        r"%APPDATA%\Spotify\Spotify.exe"
    ),

    "discord": os.path.expandvars(
        r"%LOCALAPPDATA%\Discord\Update.exe --processStart Discord.exe"
    ),

    "telegram": os.path.expandvars(
        r"%APPDATA%\Telegram Desktop\Telegram.exe"
    ),

    "steam": os.path.expandvars(
        r"%PROGRAMFILES(X86)%\Steam\Steam.exe"
    ),

    "whatsapp": "start whatsapp:"
}


# ======================================
# NORMALIZE TEXT
# ======================================

import re


def normalize_text(text):

    text = text.lower().strip()

    text = re.sub(
        r"[^\w\s]",
        "",
        text
    )

    # ==================================
    # WHISPER FIXES
    # ==================================

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

        "chalu karo": "open",
        "start karo": "open",
    }

    for wrong, correct in replacements.items():

        text = text.replace(
            wrong,
            correct
        )

    # ==================================
    # KEEP SEARCH COMMANDS INTACT
    # ==================================

    search_words = [

        "search",
        "play",
        "find",
        "look up"
    ]

    if any(
        word in text
        for word in search_words
    ):
        return text

    # ==================================
    # OPEN SHORTCUTS
    # ==================================

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
        "vscode": "open vscode",
        "vs code": "open vscode",
    }

    for key, value in shortcuts.items():

        if (
            text == key
            or text.endswith(key)
        ):

            return value

    return text
# ======================================
# OPEN APP
# ======================================

def open_app(app_name):

    command = APP_PATHS.get(app_name)

    if not command:
        return None

    try:

        if command.startswith("start"):

            os.system(command)

        else:

            subprocess.Popen(
                command,
                shell=True
            )

        return f"Opening {app_name.title()}"

    except Exception:

        return f"{app_name.title()} not found"


# ======================================
# SEARCH
# ======================================

def search_google(query):

    webbrowser.open(
        f"https://www.google.com/search?q={query}"
    )

    return (
        f"Searching for {query}"
    )


def search_youtube(query):

    webbrowser.open(
        f"https://www.youtube.com/results?"
        f"search_query={query}"
    )

    return (
        f"Searching {query} on YouTube"
    )


# ======================================
# EXECUTE COMMAND
# ======================================

def execute_command(text):

    text = normalize_text(text)

    print(
        f"Normalized command: {text}"
    )

    # ==================================
    # YOUTUBE SEARCH
    # ==================================

    youtube_patterns = [

        "search",
        "play",
        "youtube"
    ]

    if (
        "youtube" in text
        and any(
            x in text
            for x in youtube_patterns
        )
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
                word,
                ""
            )

        query = query.strip()

        if query:

            return search_youtube(
                query
            )

    # ==================================
    # GOOGLE SEARCH
    # ==================================

    if (
        text.startswith("search ")
        or text.startswith("google ")
    ):

        query = text

        for word in [

            "search",
            "google",
            "open"
        ]:

            query = query.replace(
                word,
                ""
            )

        query = query.strip()

        if query:

            return search_google(
                query
            )

    # ==================================
    # OPEN WEBSITE
    # ==================================

    websites = {

        "youtube":
        "https://youtube.com",

        "google":
        "https://google.com",

        "github":
        "https://github.com",

        "gmail":
        "https://mail.google.com",

        "chatgpt":
        "https://chat.openai.com",

        "linkedin":
        "https://linkedin.com",

        "instagram":
        "https://instagram.com",

        "facebook":
        "https://facebook.com",

        "twitter":
        "https://twitter.com",
    }

    for name, url in websites.items():

        if (
            f"open {name}" in text
            or text == name
        ):

            webbrowser.open(url)

            return (
                f"Opening {name.title()}"
            )

    # ==================================
    # OPEN APPS
    # ==================================

    for app in APP_PATHS.keys():

        if (
            f"open {app}" in text
            or text == app
        ):

            return open_app(app)

    # ==================================
    # FOLDERS
    # ==================================

    folders = {

        "downloads":
        os.path.join(
            os.path.expanduser("~"),
            "Downloads"
        ),

        "documents":
        os.path.join(
            os.path.expanduser("~"),
            "Documents"
        ),

        "desktop":
        os.path.join(
            os.path.expanduser("~"),
            "Desktop"
        ),
    }

    for name, path in folders.items():

        if (
            f"open {name}" in text
        ):

            subprocess.Popen(
                f'explorer "{path}"'
            )

            return (
                f"Opening {name}"
            )

    # ==================================
    # SYSTEM COMMANDS
    # ==================================

    if "shutdown" in text:

        os.system(
            "shutdown /s /t 5"
        )

        return (
            "Shutting down PC"
        )

    if "restart" in text:

        os.system(
            "shutdown /r /t 5"
        )

        return (
            "Restarting PC"
        )

    if "lock pc" in text:

        os.system(
            "rundll32.exe user32.dll,LockWorkStation"
        )

        return (
            "Locking PC"
        )

    # ==================================
    # VOLUME
    # ==================================

    if "mute" in text:

        os.system(
            "nircmd.exe mutesysvolume 1"
        )

        return "Muted"

    if "volume up" in text:

        os.system(
            "nircmd.exe changesysvolume 5000"
        )

        return "Volume increased"

    if "volume down" in text:

        os.system(
            "nircmd.exe changesysvolume -5000"
        )

        return "Volume decreased"

    return None