import json
import os
import re


MEMORY_FILE = "memory.json"


# ==================================
# LOAD MEMORY
# ==================================

def load_memory():

    if not os.path.exists(
        MEMORY_FILE
    ):
        return {}

    try:

        with open(
            MEMORY_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except Exception:

        return {}


# ==================================
# SAVE MEMORY
# ==================================

def save_memory(data):

    with open(
        MEMORY_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=4
        )


# ==================================
# REMEMBER
# ==================================

def remember(text):

    text = text.lower().strip()

    memory = load_memory()

    # =================================
    # PROJECT MEMORY FIRST
    # =================================

    project_patterns = [

        r"i am building (.+)",
        r"im building (.+)",
        r"my project is (.+)",
    ]

    for pattern in project_patterns:

        match = re.search(
            pattern,
            text
        )

        if match:

            project = (
                match.group(1)
                .strip()
                .title()
            )

            memory["project"] = project

            save_memory(
                memory
            )

            return (
                f"I will remember "
                f"your project "
                f"{project}"
            )

    # =================================
    # NAME MEMORY
    # =================================

    name_patterns = [

        r"my name is (.+)",
        r"call me (.+)",
    ]

    for pattern in name_patterns:

        match = re.search(
            pattern,
            text
        )

        if match:

            name = (
                match.group(1)
                .strip()
                .title()
            )

            # Prevent bad memory
            blocked_words = {

                "building",
                "project",
                "python",
                "code"
            }

            if (
                name.lower()
                not in blocked_words
            ):

                memory["name"] = name

                save_memory(
                    memory
                )

                return (
                    f"Nice to meet "
                    f"you {name}"
                )

    return None


# ==================================
# RECALL MEMORY
# ==================================

def recall(text):

    text = text.lower().strip()

    memory = load_memory()

    # =================================
    # NAME RECALL
    # =================================

    if any(
        x in text
        for x in [

            "what is my name",
            "do you know my name",
            "tell me my name"
        ]
    ):

        if "name" in memory:

            return (
                f"Your name is "
                f"{memory['name']}"
            )

        return (
            "I don't know "
            "your name yet."
        )

    # =================================
    # PROJECT RECALL
    # =================================

    if any(
        x in text
        for x in [

            "what am i building",
            "what project am i building",
            "what is my project"
        ]
    ):

        if "project" in memory:

            return (
                f"You are building "
                f"{memory['project']}"
            )

        return (
            "I don't know "
            "your project yet."
        )

    return None