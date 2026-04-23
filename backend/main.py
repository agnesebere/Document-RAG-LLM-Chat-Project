from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from scripts.AIChat import (
    retrieve_context,
    ask_mistral,
    format_memory
)
from scripts.memory_utils import (
    get_customer_memory,
    update_customer_memory
)
from scripts.guardrails import (
    is_sensitive_query,
    is_out_of_scope_query,
    fallback_response,
    escalation_response,
    out_of_scope_response
)


app = FastAPI(title="SecureBank Support API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    customer_id: str
    message: str


class ChatResponse(BaseModel):
    answer: str


def has_sufficient_context(context: str) -> bool:
    return bool(context and len(context.strip()) > 80)


@app.get("/")
def root():
    return {"message": "SecureBank Support API is running"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    customer_id = request.customer_id.strip()
    query = request.message.strip()

    customer_memory = get_customer_memory(customer_id)
    memory_text = format_memory(customer_memory["history"])

    # Guardrail 1: out of scope
    if is_out_of_scope_query(query):
        answer = out_of_scope_response()
        update_customer_memory(customer_id, query, answer)
        return ChatResponse(answer=answer)

    # Retrieve context
    context = retrieve_context(query)

    # Guardrail 2: insufficient context
    if not has_sufficient_context(context):
        answer = fallback_response()
        update_customer_memory(customer_id, query, answer)
        return ChatResponse(answer=answer)

    # Generate answer
    answer = ask_mistral(query, context, memory_text)

    # Guardrail 3: escalation
    if is_sensitive_query(query):
        answer = answer + "\n\n" + escalation_response()

    update_customer_memory(customer_id, query, answer)

    return ChatResponse(answer=answer)