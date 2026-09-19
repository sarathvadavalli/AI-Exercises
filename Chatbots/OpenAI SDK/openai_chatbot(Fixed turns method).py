from openai import OpenAI
import time

REQUESTY_API_KEY = "<key>"
MAX_RETRIES = 3
MAX_MESSAGE_LIMIT = 3


client = OpenAI(
    #base_url="https://openrouter.ai/api/v1",
    base_url="https://router.requesty.ai/v1",
    api_key=REQUESTY_API_KEY
)

def trim_history(messages, max_messages):
    if len(messages) > max_messages:
        k = max_messages if max_messages % 2 == 1 else max_messages-1
        return messages[-k:]

    return messages


if __name__ == "__main__":
    # Initialize conversation history list
    messages = [
        {
            "role": "system",
            "content": "You are a helpful programming assistant."
        }
    ]

    print("--- Chatbot Initialized (type 'quit' or 'exit' to stop) ---")

    while True:
        # 1. Get user input
        user_input = input("\nUser: ").strip()

        # 2. Check for exit command
        if user_input.lower() in ["quit", "exit"]:
            print("Bot: Goodbye!")
            break

        # 3. Skip empty inputs
        if not user_input:
            continue

        # 4. Append user message to history
        messages.append({"role": "user", "content": user_input})

        # 5. Remove the older conversation history that exceeds window limit
        convo = messages[1:]
        messages = messages[0] + trim_history(convo, max_messages=MAX_MESSAGE_LIMIT)

        request_failed = False
        for attempt in range(MAX_RETRIES + 1):
            has_generated = False
            try:
                # 6. Send a request to the API
                response = client.chat.completions.create(
                    model="google/gemma-4-31b-it",
                    messages=messages,
                    stream=True
                    # extra_body={"reasoning": {"enabled": True}}
                )

                chunks = []
                print("Bot: ", end="")
                
                # 7. Display content in each chunk received from llm
                for chunk in response:
                    content = chunk.choices[0].delta.content if chunk.choices and chunk.choices[0].delta.content else ""
                    
                    if content:
                        print(content, end="", flush=True)
                        has_generated = True
                        chunks.append(content)

                answer = "".join(chunks)

                # 8. Append assistant response to history
                messages.append({"role": "assistant", "content": answer})
                break

            except Exception as e:
                print(f"Error: {e}")
                if has_generated:
                    request_failed = True
                    print("[Response interrupted]")
                    break

                if attempt < MAX_RETRIES:
                    delay = 2 ** (attempt)
                    print(f"Retrying in {delay} seconds...")
                    time.sleep(delay)
                else:
                    request_failed = True
                    print("[Request failed]")
            
        if request_failed == True:
            messages.pop()

    print(messages)