import os
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import PydanticOutputParser

from typing import Literal
from summarization_schema import Summary
from template import get_summarizer_prompt
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('API_KEY')

def summarize_text(
    text: str,
    target_size: Literal["Small", "Medium", "Detailed"],
) -> Summary:

    model = ChatOpenAI(
        base_url="https://router.requesty.ai/v1",
        api_key=api_key,
        model="google/gemma-4-31b-it",
    )

    parser = PydanticOutputParser(pydantic_object=Summary)

    prompt = get_summarizer_prompt(parser)

    chain = prompt | model | parser

    response = chain.invoke({
        "text": text,
        "length": target_size
    })

    return Summary.model_validate(response)