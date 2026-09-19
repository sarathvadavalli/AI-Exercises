from google import genai
import json
from algorithm import get_clean_history

api_key = "<key>"
client = genai.Client(api_key=api_key)

chat = client.chats.create(model="gemini-3.6-flash")

clean_history = []
while True:
    qn = input('User: ')
    if qn.lower() == 'exit':
        print('Gemini: Good bye! Have a nice day.')
        break

    clean_history.append({'role': 'user', 'content': qn})
    print("Gemini: ", end="")
    try:
        stream = chat.send_message_stream(qn)
        chunks = []
        for chunk in stream:
            if chunk.text:
                chunks.append(chunk.text)
                print(chunk.text)

        response = ''.join(chunks)
        clean_history.append({'role': 'model', 'content': response})
    except Exception as e:
        clean_history.pop()
        print(f"An error occurred: {e.message}")

# Save clean history to the file in json format
with open("chat_history_clean1.json", "w", encoding="utf-8") as f:
    json.dump(clean_history, f, indent=2)


history = chat.get_history()
with open('chat_history.txt', 'w') as f:
    f.write(str(history))

clean_history_parsed = get_clean_history(history)

# Save clean history to the file in json format
with open("chat_history_clean2.json", "w", encoding="utf-8") as f:
    json.dump(clean_history_parsed, f, indent=2)