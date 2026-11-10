import os
from dotenv import load_dotenv

# 1. Load environment variables
load_dotenv()

# 2. Validate API keys
required_keys = [
    "GROQ_API_KEY",
    "FREECRYPTO_TOKEN",
    "NEWSAPI_KEY"
]

missing_keys = [
    key for key in required_keys
    if not os.getenv(key)
]

if missing_keys:
    raise EnvironmentError(
        f"Missing environment variables: {', '.join(missing_keys)}"
    )

print("All API keys loaded successfully!")

# 3. Import the agent after loading the environment
from agent.graph import run_agent


# 4. Run the application
if __name__ == "__main__":
    print("\n===== CRYPTO ANALYSIS AGENT =====")

    question = input("\nAsk your crypto question: ")

    print("\nAnalyzing...\n")

    try:
        answer = run_agent(question)
        print("===== AGENT RESPONSE =====")
        print(answer)

    except Exception as e:
        print(f"An error occurred: {e}")