import json
from pathlib import Path


MEMORY_PATH = Path("memory/customer_memory.json")


def load_memory():
    if not MEMORY_PATH.exists():
        return {}
    with open(MEMORY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_memory(memory_data):
    MEMORY_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(MEMORY_PATH, "w", encoding="utf-8") as f:
        json.dump(memory_data, f, indent=2)


def get_customer_memory(customer_id):
    memory_data = load_memory()
    return memory_data.get(customer_id, {
        "profile": {},
        "history": []
    })


def update_customer_memory(customer_id, user_query, bot_answer):
    memory_data = load_memory()

    if customer_id not in memory_data:
        memory_data[customer_id] = {
            "profile": {},
            "history": []
        }

    memory_data[customer_id]["history"].append({
        "user_query": user_query,
        "bot_answer": bot_answer
    })

    # Keep only last 5 interactions for now
    memory_data[customer_id]["history"] = memory_data[customer_id]["history"][-5:]

    save_memory(memory_data)