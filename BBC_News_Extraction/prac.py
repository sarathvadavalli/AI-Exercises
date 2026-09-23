from nltk.tokenize import sent_tokenize
import nltk
nltk.download('punkt_tab')

# Example text (typically a paragraph)
text = "This is a sentence. Here is another one. And a third one."

# Chunk text into sentences
chunks = sent_tokenize(text)

# Display the chunks
for i, chunk in enumerate(chunks):
    print(f"Sentence {i + 1}: {chunk}")