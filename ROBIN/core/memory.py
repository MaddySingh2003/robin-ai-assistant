import sys
try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except AttributeError:
    pass

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

    # ------------------------------
    # SAVE PROJECT
    # ------------------------------

    project_patterns = [

        r"i am building (.+)",
        r"im building (.+)",
        r"i am making (.+)",
        r"i am developing (.+)",
        r"my project is (.+)"
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

            save_memory(memory)

            return (
                f"I will remember your project {project}"
            )

    # ------------------------------
    # SAVE NAME
    # ------------------------------

    name_patterns = [

        r"my name is (.+)",
        r"i am (.+)",
        r"im (.+)",
        r"call me (.+)"
    ]

    for pattern in name_patterns:

        match = re.search(
            pattern,
            text
        )

        if match:

            value = (
                match.group(1)
                .strip()
                .title()
            )

            bad_values = {

                "Building",
                "Making",
                "Developing",
                "Learning",
                "Coding"
            }

            if value not in bad_values:

                memory["name"] = value

                save_memory(memory)

                return (
                    f"Nice to meet you {value}"
                )

    return None


# ==================================
# RECALL
# ==================================

def recall(text):

    text = text.lower().strip()

    memory = load_memory()

    words = set(
        re.findall(
            r"\b\w+\b",
            text
        )
    )

    # ------------------------------
    # NAME RECALL
    # ------------------------------

    if (
        "name" in words
        and (
            "my" in words
            or "what" in words
        )
    ):

        if "name" in memory:

            return (
                f"Your name is "
                f"{memory['name']}"
            )

        return (
            "I don't know your name yet."
        )

    # ------------------------------
    # PROJECT RECALL
    # ------------------------------

    project_words = {

        "project",
        "building",
        "build",
        "making",
        "developing"
    }

    if words.intersection(
        project_words
    ):

        if "project" in memory:

            return (
                f"You are building "
                f"{memory['project']}"
            )

        return (
            "I don't know your project yet."
        )

    return None


# ==================================
# CLEAR MEMORY
# ==================================

def clear_memory():

    save_memory({})


# ==================================
# DEBUG
# ==================================

if __name__ == "__main__":

    print(
        load_memory()
    )