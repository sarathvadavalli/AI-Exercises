from openai import OpenAI
import time, json
from pathlib import Path

# REQUESTY_API_KEY = "<key>"
REQUESTY_API_KEY = "rqsty-sk-115c9lZGRyCpyoqpcnzrjQOMs8yN0alSBmC5AyP2eTWGnUpbDvTQOke1DtLA52Pj7X7sUVokQuPSuB+tGKI8iGyqvqQ1/akk84CoqFC/FQY="
MAX_RETRIES = 3
CONTEXT_LIMIT = 70
SYSTEM_PROMPT_TOKENS = 6
SUMMARY_LIMIT = 24
OUTPUT_LIMIT = 20
TARGET_TOKENS = CONTEXT_LIMIT - (SYSTEM_PROMPT_TOKENS + SUMMARY_LIMIT + OUTPUT_LIMIT)

root_path = Path(__file__).parent

client = OpenAI(
    #base_url="https://openrouter.ai/api/v1",
    base_url="https://router.requesty.ai/v1",
    api_key=REQUESTY_API_KEY
)

def calculate_tokens(message: dict):
    return len(message['content'].split())


def calculate_total_tokens(messages: list[dict]):
    tokens = 0
    for message in messages:
        tokens += len(message['content'].split())

    return tokens


def summarize_conversation(old_summary: str, messages_to_summarize: list[dict]) -> str:
    prompt = f"""Summarize the key information, decisions, and context from this conversation snippet.
Combine it with the existing summary if provided. Keep it concise, factual, and focused on maintaining state for future turns.

Existing Summary:
{old_summary if old_summary else "None"}
New Conversation Snippet:
{messages_to_summarize}"""

    for attempt in range(MAX_RETRIES + 1):
        try:
            response = client.chat.completions.create(
                model="google/gemma-4-31b-it",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            if attempt < MAX_RETRIES:
                delay = 2 ** (attempt)
                time.sleep(delay)
            else:
                print(f"\n[Summarization Error: {e}]")
                return old_summary


if __name__ == "__main__":
    # Initialize conversation history list with syatem instructions
    system_instructions = "You are a helpful programming assistant."
    running_summary = ""
    messages = [system_instructions]
    history = [{
            "role": "system",
            "content": system_instructions
        }]

    print("--- Chatbot Initialized (type 'quit' or 'exit' to stop) ---")

    total_tokens = 0
    terminate = False
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
        if total_tokens > TARGET_TOKENS:
            if len(messages) >= 4:
                # Ensure split point preserves (user, assistant) pair boundaries
                half_index = (len(messages) // 2)
                if half_index % 2 != 0:
                    half_index -= 1  # Keep pair boundary even
                
                old_slice = messages[:half_index]
                total_tokens -= calculate_total_tokens(old_slice)
                messages = messages[half_index:]
                
                # Summarize all old messages at once
                running_summary = summarize_conversation(running_summary, old_slice)
            elif len(messages) >= 2:
                old_slice = messages[:2]
                total_tokens -= (calculate_tokens(messages[0]) + calculate_tokens(messages[1]))
                messages = messages[2:]
                running_summary = summarize_conversation(running_summary, old_slice)
            else:
                messages = []
                print(f"Bot: Unable to process as your input is too long..")
                exceeded = True 
                break
            
        if exceeded:
            continue

        if running_summary:
            print(running_summary)

        api_messages = [{"role": "system", "content": system_instructions},
            {"role": "system", "content": running_summary}]
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
                status_code = getattr(e, "status_code", None)
                if status_code and status_code == 403:
                    terminate = True
                    print("[Not authorized]")
                    break
                
                if status_code and status_code == 400:
                    terminate = True
                    print("[Invalid request format]")
                    break

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

        if terminate:
            messages.pop()
            history.pop()
            break
        if request_failed:
            messages.pop()
            history.pop()

    if not no_access:
        with open(f'{root_path}/openai_chatbot_history2.json', 'w') as f:
            json.dump(history, f, indent=4)
            print("Chat history successfully saved.")

    # Generated summary: The user introduced himself as Sarath. The assistant identified itself as a programming assistant.