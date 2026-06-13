import webbrowser
import os
import subprocess
import re
from tools.project_generator import (
    create_react_project,
    create_fastapi_project,
    create_node_project,
    create_nextjs_project,
    create_flask_project,
    create_python_project,
    create_cpp_project,
    create_java_project
)

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

def normalize_text(text):

    text = text.lower().strip()

    text = re.sub(
        r"[^\w\s]",
        "",
        text
    )

    replacements = {

        "grom": "chrome",
        "krom": "chrome",
        "crome": "chrome",
        "chchrome": "chrome",

        "you tube": "youtube",
        "u tube": "youtube",

        "v s code": "vscode",
        "vs code": "vscode",
        "visual studio": "vscode",

        "khol": "open",
        "kholo": "open",

        "start karo": "open",
        "chalu karo": "open",

        "perch": "search",
        "serch": "search",
    }

    for wrong, right in replacements.items():
        text = text.replace(wrong, right)

    return text.strip()


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
# SEARCH FUNCTIONS
# ======================================

def search_google(query):

    webbrowser.open(
        f"https://www.google.com/search?q={query}"
    )

    return f"Searching for {query}"


def search_youtube(query):

    webbrowser.open(
        f"https://www.youtube.com/results?search_query={query}"
    )

    return f"Searching {query} on YouTube"


# ======================================
# WINDOWS VOLUME CONTROL
# ======================================

def send_media_key(key):

    try:

        script = f"""
        (New-Object -ComObject WScript.Shell)
        .SendKeys([char]{key})
        """

        subprocess.run(
            [
                "powershell",
                "-Command",
                script
            ],
            capture_output=True
        )

        return True

    except Exception as e:

        print("Volume Error:", e)
        return False


# ======================================
# CREATE FILE IN VSCODE
# ======================================
def open_vscode(path):

    try:

        vscode = r"C:\Users\Milan\AppData\Local\Programs\Microsoft VS Code\bin\code.cmd"

        subprocess.Popen(
            [vscode, path]
        )

        print(f"Opened VS Code: {path}")

    except Exception as e:

        print("VSCode error:", e)


def create_file_in_vscode(text):

    extensions = {

        "python": ".py",
        "javascript": ".js",
        "html": ".html",
        "css": ".css",
        "java": ".java",
        "json": ".json",
        "text": ".txt"
    }

    detected_extension = ".txt"

    for lang, ext in extensions.items():

        if lang in text:
            detected_extension = ext
            break

    filename = f"new_file{detected_extension}"

    desktop = os.path.join(
        os.path.expanduser("~"),
        "Desktop"
    )

    file_path = os.path.join(
        desktop,
        filename
    )

    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as file:
        file.write("")

    subprocess.Popen(
        f'code "{file_path}"',
        shell=True
    )

    return f"Created {filename} in VSCode"

import os
import re

def create_project_file(text):

    file_types = {

        "python": ".py",
        "py": ".py",

        "javascript": ".js",
        "js": ".js",

        "typescript": ".ts",
        "ts": ".ts",

        "html": ".html",
        "css": ".css",

        "java": ".java",

        "c++": ".cpp",
        "cpp": ".cpp",

        "c ": ".c",
        " c": ".c",

        "c#": ".cs",

        "json": ".json",

        "react": ".jsx",
        "angular": ".ts",

        "node": ".js",

        "sql": ".sql",

        "txt": ".txt"
    }

    ext = None

    lower = text.lower()

    for key, value in file_types.items():

        if key in lower:
            ext = value
            break

    if not ext:
        return None

    filename = f"new_file{ext}"

    filepath = os.path.join(
        os.getcwd(),
        filename
    )

    with open(
        filepath,
        "w",
        encoding="utf-8"
    ) as f:

        f.write("")

    return (
        f"Created {filename}"
    )
# ======================================
# EXECUTE COMMAND
# ======================================
import re

def extract_project_name(text):

    match = re.search(
        r"(?:named|name)\s+(.+)",
        text.lower()
    )

    if match:

        return (
            match.group(1)
            .strip()
            .replace(" ", "_")
        )

    return None

def create_project(text):

    text = text.lower()

    name = extract_project_name(text)

    # =========================
    # REACT
    # =========================

    if (
        "react" in text
        and (
            "project" in text
            or "app" in text
        )
    ):

        return create_react_project(
            name or "ReactApp"
        )

    # =========================
    # NEXTJS
    # =========================

    if (
        "next" in text
        or "nextjs" in text
    ):

        return create_nextjs_project(
            name or "NextApp"
        )

    # =========================
    # FASTAPI
    # =========================

    if (
        "fastapi" in text
        or "fast api" in text
    ):

        return create_fastapi_project(
            name or "FastAPIApp"
        )

    # =========================
    # FLASK
    # =========================

    if "flask" in text:

        return create_flask_project(
            name or "FlaskApp"
        )

    # =========================
    # NODE
    # =========================

    if (
        "node" in text
        or "express" in text
    ):

        return create_node_project(
            name or "NodeApp"
        )

    # =========================
    # PYTHON
    # =========================

    if (
        "python project" in text
        or "python app" in text
    ):

        return create_python_project(
            name or "PythonApp"
        )

    # =========================
    # C++
    # =========================

    if (
        "c++" in text
        or "cpp" in text
    ):

        return create_cpp_project(
            name or "CppProject"
        )

    # =========================
    # JAVA
    # =========================

    if "java" in text:

        return create_java_project(
            name or "JavaApp"
        )

    return None
    
    

def execute_command(text):
    try:

      project_result = create_project(text)
      if project_result:
            return project_result

    except Exception as e:

      print("Project Error:", e)

      return f"Project creation failed: {e}"

    text = normalize_text(text)
    # =========================
# PROJECT COMMANDS
# =========================

    project_result = create_project(text)

    if project_result:
      return project_result

    print(
        f"Normalized command: {text}"
    )

    # ==================================
    # CREATE FILE IN VSCODE
    # ==================================

    if (
        "create" in text
        and "file" in text
        and "vscode" in text
    ):

        return create_file_in_vscode(text)

    # ==================================
    # YOUTUBE SEARCH
    # ==================================

    if "youtube" in text and (

        "search" in text
        or "play" in text
        or "find" in text
    ):

        query = text

        remove_words = [

            "search",
            "play",
            "find",
            "youtube",
            "on youtube",
            "open"
        ]

        for word in remove_words:
            query = query.replace(word, "")

        query = query.strip()

        if query:
            return search_youtube(query)

    # ==================================
    # GOOGLE SEARCH
    # ==================================
    if "open" in text and "project" in text:

      project_name = (
        text
        .replace("open", "")
        .replace("project", "")
        .strip()
        .replace(" ", "_")
    )

      path = os.path.join(
        get_projects_folder(),
        project_name
    )

      if os.path.exists(path):

        open_vscode(path)

        return f"Opening {project_name}"

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
            query = query.replace(word, "")

        query = query.strip()

        if query:
            return search_google(query)

    # ==================================
    # OPEN WEBSITES
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
    }
    

    for name, url in websites.items():

        if (
            f"open {name}" in text
            or text == name
        ):

            webbrowser.open(url)

            return f"Opening {name.title()}"

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
    # OPEN FOLDERS
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
        )
    }

    for name, path in folders.items():

        if f"open {name}" in text:

            subprocess.Popen(
                f'explorer "{path}"'
            )

            return f"Opening {name}"

    # ==================================
    # SYSTEM COMMANDS
    # ==================================

    if text == "shutdown":

        os.system(
            "shutdown /s /t 5"
        )

        return "Shutting down PC"

    if text == "restart":

        os.system(
            "shutdown /r /t 5"
        )

        return "Restarting PC"

    if "lock pc" in text:

        os.system(
            "rundll32.exe user32.dll,LockWorkStation"
        )

        return "Locking PC"

    # ==================================
    # VOLUME CONTROL
    # ==================================

    if text == "mute":

        send_media_key(173)
        return "Muted"

    if text == "unmute":

        send_media_key(173)
        return "Unmuted"

    if "volume up" in text:

        for _ in range(5):
            send_media_key(175)

        return "Volume increased"

    if "volume down" in text:

        for _ in range(5):
            send_media_key(174)

        return "Volume decreased"
    

    return None