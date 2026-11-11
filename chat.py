
from agent.graph import run_agent


def main():
    thread_id = "crypto-chat-session-1"

    print("\n========================================")
    print("       CRYPTO ANALYSIS AGENT")
    print("========================================")
    print("Ask me anything about cryptocurrency!")
    print("Type 'exit' or 'quit' to stop.")
    print("----------------------------------------")

    while True:
        try:
            question = input("\nYou: ").strip()

            if question.lower() in ["exit", "quit"]:
                print("\nAgent: Goodbye! Happy investing!")
                break

            if not question:
                continue

            print("\nAgent: ", end="", flush=True)

            response = run_agent(
                question=question,
                thread_id=thread_id
            )

            print(response)

        except KeyboardInterrupt:
            print("\n\nAgent: Chat interrupted. Goodbye!")
            break

        except Exception as e:
            print(f"\nError: {e}")


if __name__ == "__main__":
    main()
