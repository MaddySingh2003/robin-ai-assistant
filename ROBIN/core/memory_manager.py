import re

from core.chroma_memory import (
    save_memory,
    search_memory
)


# ==========================
# SAVE FACTS
# ==========================

def auto_save_memory(text):

    text = text.strip().lower()

    patterns = [

        "my name is",
        "call me",

        "i am building",
        "i am making",
        "i am developing",

        "my project is",

        "remember that",

        "i like",
        "i prefer",
        "i use"
    ]

    if any(
        pattern in text
        for pattern in patterns
    ):

        save_memory(
            text,
            memory_type="fact"
        )

        print(
            f"💾 Saved memory: {text}"
        )


# ==========================
# MEMORY CONTEXT FOR AI
# ==========================

def get_memory_context(query):

    memories = search_memory(
        query,
        top_k=3
    )

    filtered = []

    for m in memories:

        if len(m.strip()) > 10:
            filtered.append(m)

    return "\n".join(filtered)

# ==========================
# SMART RECALL
# ==========================

def recall_memory(query):

    query = query.lower().strip()

    memories = search_memory(
        query,
        top_k=10
    )

    if not memories:
        return None

    # ----------------------
    # USER NAME
    # ----------------------

    if (
        "what is my name" in query
        or "tell me my name" in query
        or "do you know my name" in query
    ):

        for memory in memories:

            match = re.search(
                r"my name is (.+)",
                memory,
                re.IGNORECASE
            )

            if match:

                return (
                    f"Your name is "
                    f"{match.group(1).title()}"
                )

    # ----------------------
    # USER PROJECT
    # ----------------------

    if (
        "what is my project" in query
        or "what am i building" in query
        or "which project" in query
    ):

        for memory in memories:

            if (
                "i am building" in memory.lower()
                or "my project is" in memory.lower()
            ):

                return (
                    f"I remember that "
                    f"{memory}"
                )

    return None