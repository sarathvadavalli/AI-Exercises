from dataclasses import dataclass, field
from typing import List, Optional
import json


def get_content(parts):
    text_parts = [part.text for part in parts if part.text]
    return ''.join(text_parts)

def get_clean_history(history):
    clean_history = []
    temp = []
    for i in range(len(history)-1):
        role = history[i].role
        parts = history[i].parts

        if(role == 'user'):
            total_content = get_content(parts)
            clean_history.append({'role': 'user', 'content': total_content})
        else:
            temp.append(get_content(parts))
            if history[i+1].role == 'user':
                clean_history.append({'role': 'model', 'content': ''.join(temp)})
                temp = []

    n = len(history)
    role = history[n-1].role
    parts = history[n-1].parts
    if(role == 'user'):
        total_content = get_content(parts)
        clean_history.append({'role': 'user', 'content': total_content})
    else:
        temp.append(get_content(parts))
        clean_history.append({'role': 'model', 'content': ''.join(temp)})

    return clean_history

# @dataclass
# class Part:
#     text: Optional[str] = ""
#     thought_signature: Optional[bytes] = None

# @dataclass
# class Content:
#     parts: List[Part] = field(default_factory=list)
#     role: str = "model"

# @dataclass
# class UserContent(Content):
#     def __post_init__(self):
#         self.role = "user"