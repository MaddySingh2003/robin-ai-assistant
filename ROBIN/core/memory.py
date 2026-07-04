import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except AttributeError:
    pass

"""
Legacy memory compatibility layer.

Memory is now stored in ChromaDB through code_manager.py.
Older code importing remember() and recall()
will continue working.
"""

from core.code_manager import (
    remember,
    recall
)


def clear_memory():
    """
    Placeholder.
    Chroma memory clearing should be handled
    directly from chroma_memory.py.
    """
    print("⚠️ clear_memory() not implemented for ChromaDB")


def load_memory():
    """
    Compatibility stub.
    """
    return {}


def save_memory(data):
    """
    Compatibility stub.
    """
    pass


if __name__ == "__main__":

    print("Memory backend: ChromaDB")