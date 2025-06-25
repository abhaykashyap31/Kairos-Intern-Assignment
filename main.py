from agent_host import AgentHost

def main():
    """Entry point for the CLI chat interface. Handles user input and displays streamed responses from the agent host."""
    agent = AgentHost()
    print("Welcome to Scientific‑Paper Scout! Type 'quit' to exit.")
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ("quit", "exit"): break
        response_stream = agent.handle_user_message(user_input)
        print("Assistant:")
        for line in response_stream:
            print(line)

if __name__ == "__main__":
    main() 