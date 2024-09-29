from typing import Any, Callable, Dict, Optional
from openai import OpenAI
from config import AppConfig

from guardrails.validator_base import (
    FailResult,
    PassResult,
    ValidationResult,
    Validator,
    register_validator,
)

API_SECRET_KEY = AppConfig.OPENAI_API_SECRET_KEY
BASE_URL = AppConfig.OPENAI_API_SECRET_KEY

@register_validator(name="guardrails/self_exam", data_type="string")
class SelfExam(Validator):
    def __init__(
        self,
        api_key = str,
        base_url = str,
        on_fail: Optional[Callable] = None,
    ):
        super().__init__(
            on_fail=on_fail
            )
        self.api_key = api_key
        self.url = base_url
        
    def validate(self, value: Any, metadata: Dict) -> ValidationResult:
        check_user_prompt = f"Does the following text contain harmful content: {value} \nRespond with 'Yes, this is harmful' or 'No, this is not harmful'."
        client = OpenAI(api_key=self.api_key, base_url=self.url)
        resp = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": check_user_prompt}
            ]
        )
        if 'yes' in resp.choices[0].message.content.lower():
            return FailResult(
                error_message="The generated text contains harmful content.",
                fix_value="",
            )
        elif 'no' in resp.choices[0].message.content.lower():
            return PassResult()
        else:
            print('Self-exam failed!')
        return PassResult()