
from agent.graph import run_agent

print("\n===== CRYPTO AGENT MEMORY TEST =====")

# First conversation turn
response1 = run_agent(
    "My name is Eya and I am interested in Bitcoin.",
    thread_id="test-thread-1"
)

print("\nAgent:", response1)


# Second conversation turn
response2 = run_agent(
    "What is my name and which cryptocurrency am I interested in?",
    thread_id="test-thread-1"
)

print("\nAgent:", response2)


# New conversation with a different thread ID
response3 = run_agent(
    "What is my name?",
    thread_id="test-thread-2"
)

print("\nAgent (new conversation):", response3)
