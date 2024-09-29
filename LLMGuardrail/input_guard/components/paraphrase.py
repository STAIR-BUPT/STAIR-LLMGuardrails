from typing import Any, Callable, Dict, Optional
from openai import OpenAI

from guardrails.validator_base import (
    FailResult,
    PassResult,
    ValidationResult,
    Validator,
    register_validator,
)

class Paraphrase():
    def __init__(
        self,
        api_key = str,
        base_url = str
    ):
        self.api_key = api_key
        self.base_url = base_url
        
    def validate(self, value: Any) -> str:
        input_prompt_paraphrase = "Please paraphrase the following sentences. Give me paraphrased results only. Do not include any other information.\n" + value
        client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        resp = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": input_prompt_paraphrase}
            ]
        )
        value = resp.choices[0].message.content
        return value