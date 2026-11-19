from pydantic import BaseModel, Field
from typing import List

class Summary(BaseModel):
    summary: str = Field(description="The summarized text")
    key_points: List[str] = Field(
        description="The 3 most important points from the content"
    )
    topic: str = Field(description="The main topic of the content")