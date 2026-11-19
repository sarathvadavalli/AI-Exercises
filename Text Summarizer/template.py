from langchain_core.prompts import PromptTemplate

template = """
You are a text summarization assistant.
Your task is to summarize the provided content based on the given summary length.

Summary Length:
- Short: 50-100 words
- Medium: 150-200 words (Default)
- Detailed: 300-400 words

Instructions:
1. Ensure the summary is concise and clear.
2. Retain all important information.
3. Remove redundant information.
4. Maintain the original context and intent.
5. Do not add, assume, infer or fabricate information.
6. If the content is invalid or insufficient, return the following:
   - summary: "Unable to generate a summary. The provided content does not contain sufficient meaningful information."
   - key_points: []
   - topic: "Unknown"

Content:
{text}

Summary Length: 
{length}

{format_instructions}
"""


def get_summarizer_prompt(parser):
    return PromptTemplate(
        template=template,
        input_variables=["text", "length"],
        partial_variables={
            "format_instructions": parser.get_format_instructions()
        }
    )