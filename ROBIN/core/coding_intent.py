import re

PROGRAMMING_WORDS = [

    # languages
    "python",
    "java",
    "javascript",
    "typescript",
    "c++",
    "cpp",
    "c#",
    "c sharp",
    "c",
    "html",
    "css",
    "sql",
    "php",
    "go",
    "rust",
    "swift",
    "kotlin",

    # frameworks
    "react",
    "angular",
    "vue",
    "node",
    "nodejs",
    "express",
    "django",
    "flask",
    "fastapi",
    "tailwind",
    "bootstrap",

    # coding terms
    "api",
    "database",
    "backend",
    "frontend",
    "server",
    "function",
    "loop",
    "array",
    "list",
    "dictionary",
    "object",
    "class",
    "oops",
    "recursion",
    "bug",
    "error",
    "fix",
    "debug",
    "compile",
    "algorithm",
    "data structure",

    # coding actions
    "code",
    "program",
    "coding",
    "build",
    "create project",
    "make website",
    "login page",
]


EXPLAIN_WORDS = [

    "explain",
    "what is",
    "what's",
    "tell me",
    "batao",
    "samjhao",
    "samjha",
    "kaise",
    "kya hai",
    "how to",
    "guide",
    "teach",
]

def detect_coding_intent(text):
    text = text.lower().strip()

    has_programming=any(
        word in text for word in PROGRAMMING_WORDS
    )

    has_explain=any(
        word in text for word in EXPLAIN_WORDS
    )

    return has_programming or has_explain