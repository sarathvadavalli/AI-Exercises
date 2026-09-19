from openai import OpenAI
import time, json

REQUESTY_API_KEY = "<key>"
MAX_RETRIES = 3
CONTEXT_LIMIT = 46
SYSTEM_PROMPT_TOKENS = 6
OUTPUT_LIMIT = 20
TARGET_TOKENS = CONTEXT_LIMIT - (SYSTEM_PROMPT_TOKENS + OUTPUT_LIMIT)


client = OpenAI(
    #base_url="https://openrouter.ai/api/v1",
    base_url="https://router.requesty.ai/v1",
    api_key=REQUESTY_API_KEY
)

def calculate_tokens(message: dict):
    return len(message['content'].split())


if __name__ == "__main__":

    # Initialize conversation history list with syatem instructions
    system_instructions = "You are a helpful programming assistant."
    running_summary = ""
    messages = []
    history = [{
            "role": "system",
            "content": system_instructions
        }]

    print("--- Chatbot Initialized (type 'quit' or 'exit' to stop) ---")

    total_tokens = 0
    while True:
        # Get user input
        user_input = input("\nUser: ").strip()

        # Check for exit command
        if user_input.lower() in ["quit", "exit"]:
            print("Bot: Goodbye!")
            break

        # Skip empty inputs
        if not user_input:
            continue

        # Append user message to history
        message = {"role": "user", "content": user_input}
        messages.append(message)
        history.append(message)

        total_tokens += calculate_tokens(message)

        # Remove the older conversation history that exceeds window limit
        exceeded = False
        while total_tokens > TARGET_TOKENS:
            if len(messages) > 2:
                total_tokens -= (calculate_tokens(messages[0]) + calculate_tokens(messages[1]))
                messages = messages[2:]
            else:
                messages = []
                print(f"Bot: Unable to process as your input is too long..")
                exceeded = True 
                break

        if exceeded:
            continue 

        api_messages = [{"role": "system", "content": system_instructions}]
        api_messages = api_messages + messages
        
        request_failed = False
        for attempt in range(MAX_RETRIES + 1):
            has_generated = False
            try:
                # Send a request to the API
                response = client.chat.completions.create(
                    model="google/gemma-4-31b-it",
                    messages=api_messages,
                    stream=True
                    # extra_body={"reasoning": {"enabled": True}}
                )

                chunks = []
                print("Bot: ", end="")
                
                # Display content in each chunk received from llm
                for chunk in response:
                    content = chunk.choices[0].delta.content if chunk.choices and chunk.choices[0].delta.content else ""
                    
                    if content:
                        print(content, end="", flush=True)
                        has_generated = True
                        chunks.append(content)

                answer = "".join(chunks)

                # Append assistant response to history
                message = {"role": "assistant", "content": answer}
                messages.append(message)
                history.append(message)
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
            history.pop()

    with open('openai_chatbot_history1.json', 'w') as f:
        json.dump(history, f, indent=4)
        print("Chat history successfully saved.")