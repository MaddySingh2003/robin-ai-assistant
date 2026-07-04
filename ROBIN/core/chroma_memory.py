import sys
try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except AttributeError:
    pass

import chromadb
import uuid

client = chromadb.PersistentClient(
    path="./memory_db"
)

collection = client.get_or_create_collection(
    name="robin_memory"
)


def save_memory(
    text,
    memory_type="general"
):

    text = text.strip()

    if not text:
        return

    collection.add(
        ids=[
            str(uuid.uuid4())
        ],
        documents=[
            text
        ],
        metadatas=[
            {
                "type": memory_type
            }
        ]
    )

    print(
        f"💾 Saved memory: {text}"
    )


def search_memory(
    query,
    top_k=3
):

    try:

        results = collection.query(
            query_texts=[
                query
            ],
            n_results=top_k
        )

        docs = results.get(
            "documents",
            [[]]
        )[0]

        return docs

    except Exception as e:

        print(
            "❌ Memory search error:",
            e
        )

        return []


def memory_count():

    return collection.count()