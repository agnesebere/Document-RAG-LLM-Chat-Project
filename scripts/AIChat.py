import os
from dotenv import load_dotenv
from mistralai.client import Mistral
from qdrant_client import QdrantClient
from scripts.memory_utils import get_customer_memory, update_customer_memory
from scripts.guardrails import (
    is_sensitive_query,
    is_out_of_scope_query,
    fallback_response,
    escalation_response,
    out_of_scope_response
)

load_dotenv()

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
MODEL_NAME = "mistral-large-latest"

llm = Mistral(api_key=MISTRAL_API_KEY)
EMBED_MODEL = "mistral-embed"

# Connect to Qdrant (Cloud)
client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)

COLLECTION_NAME = "securebank_docs"


def has_sufficient_context(context: str) -> bool:
    return bool(context and len(context.strip()) > 80)


def retrieve_context(query: str) -> str:
    # Perform a semantic search to retrieve relevant bank documentation
    # Use Mistral API for embeddings to save local memory (essential for Render/Cloud)
    resp = llm.embeddings.create(model=EMBED_MODEL, inputs=[query])
    query_vector = resp.data[0].embedding

    # Using query_points for the latest Qdrant API
    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=5
    ).points

    # Combine retrieved text chunks into a single context string
    return "\n\n".join([r.payload["text"] for r in results])


def format_memory(history):
    if not history:
        return "No previous conversation history."

    lines = []
    for item in history:
        lines.append(f"Customer: {item['user_query']}")
        lines.append(f"Assistant: {item['bot_answer']}")
    return "\n".join(lines)


def ask_mistral(query: str, context: str, memory_text: str) -> str:
    messages = [
        {
            "role": "system",
            "content": (
                "You are a professional customer support assistant for SecureBank. "
                "Answer using only the provided SecureBank knowledge base context and conversation memory. "
                "Do not make up facts. "
                "If the answer is not supported by the context, say you do not have enough information. "
                "Do not provide legal, tax, medical, or investment advice. "
                "Be clear, polite, and concise."
            ),
        },
        {
            "role": "user",
            "content": f"""
Previous conversation memory:
{memory_text}

SecureBank knowledge base context:
{context}

Customer question:
{query}
"""
        }
    ]

    response = llm.chat.complete(
        model=MODEL_NAME,
        messages=messages,
    )

    content = response.choices[0].message.content
    return content if isinstance(content, str) else str(content)


def main():
    print("SecureBank AI Chatbot Ready (with guardrails)!")

    customer_id = input("Enter customer ID: ").strip()

    while True:
        query = input("\nAsk a question (or type 'exit'): ").strip()

        if query.lower() == "exit":
            break

        customer_memory = get_customer_memory(customer_id)
        memory_text = format_memory(customer_memory["history"])

        # Guardrail 1: Out-of-scope questions
        if is_out_of_scope_query(query):
            answer = out_of_scope_response()
            print("\nAnswer:")
            print(answer)
            update_customer_memory(customer_id, query, answer)
            continue

        print("\nRetrieving context...")
        context = retrieve_context(query)

        # Guardrail 2: Weak or missing knowledge-base support
        if not has_sufficient_context(context):
            answer = fallback_response()
            print("\nAnswer:")
            print(answer)
            update_customer_memory(customer_id, query, answer)
            continue

        print("Generating answer...\n")
        answer = ask_mistral(query, context, memory_text)

        # Guardrail 3: Sensitive-topic escalation note
        if is_sensitive_query(query):
            answer = answer + "\n\n" + escalation_response()

        print("Answer:")
        print(answer)

        update_customer_memory(customer_id, query, answer)


if __name__ == "__main__":
    main()