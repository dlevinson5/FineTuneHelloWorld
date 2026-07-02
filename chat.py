import sys
import ollama

def start_chat():
    model_name = "movie-expert:latest"
    print(f"--- Starting session with '{model_name}' ---")
    print("Type 'exit' or 'quit' to end the chat.\n")

    # Initialize chat history
    messages = [
        {"role": "system", "content": "You are a movie database assistant specializing in box office numbers between 2000 and 2024."}
    ]

    while True:
        try:
            user_input = input("\nYou: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ['exit', 'quit']:
                print("Goodbye!")
                break

            messages.append({"role": "user", "content": user_input})

            print("AI: ", end="", flush=True)

            # Stream the response natively from Ollama
            response_stream = ollama.chat(
                model=model_name,
                messages=messages,
                stream=True
            )

            full_response = ""
            for chunk in response_stream:
                content = chunk['message']['content']
                print(content, end="", flush=True)
                full_response += content

            print() # Print newline at the end
            messages.append({"role": "assistant", "content": full_response})

        except KeyboardInterrupt:
            print("\nSession ended.")
            sys.exit(0)

if __name__ == "__main__":
    start_chat()