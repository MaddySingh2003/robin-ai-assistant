import re

from .chroma_memory import (
save_memory,
search_memory
)

# =====================================

# CODE GENERATION

# =====================================

def generate_code_snippet(prompt):


  snippet = f"""# Code generated for:


  # {prompt}

def main():
pass

if **name** == "**main**":
main()
"""


  save_memory(
    snippet,
    memory_type="code"
)

  return snippet


def retrieve_code_snippet(
query,
top_k=3
):
    
  return search_memory(
    query,
    top_k=top_k
)


# =====================================

# MEMORY SAVE

# =====================================

def remember(text):


  text = text.lower().strip()

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

  if not any(
    p in text
    for p in patterns
):
    return None

  save_memory(
    text,
    memory_type="fact"
)

  return "I will remember that."


# =====================================

# MEMORY RECALL

# =====================================

def recall(query):


  query = query.lower().strip()

  results = search_memory(
    query,
    top_k=10
)

  if not results:
    return None

# -----------------------------
# USER NAME
# -----------------------------

  if query in [

    "what is my name",
    "tell me my name",
    "do you know my name"
]:

    for item in results:

        match = re.search(
            r"my name is (.+)",
            item,
            re.IGNORECASE
        )

        if match:

            return (
                f"Your name is "
                f"{match.group(1).title()}"
            )

# -----------------------------
# USER PROJECT
# -----------------------------

  if query in [

    "what is my project",
    "what am i building",
    "which project am i building"
]:

    for item in results:

        if (
            "i am building" in item.lower()
            or "my project is" in item.lower()
        ):

            return (
                f"You are working on "
                f"{item}"
            )

  return None
