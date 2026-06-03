import re

from core.chroma_memory import (
    save_memory,
    search_memory
)


def auto_save_memory(text):

    text = text.strip()

    if len(text) < 8:
        return

    patterns = [

        "my name is",
        "i am building",
        "i am making",
        "my project is",
        "i am developing",
        "remember that",
        "i like",
        "i prefer",
        "i use"
    ]

    if any(
        p in text.lower()
        for p in patterns
    ):

        save_memory(
            text,
            "fact"
        )


def get_memory_context(query):

    memories = search_memory(
        query,
        top_k=5
    )

    if not memories:
        return ""

    return "\n".join(memories)