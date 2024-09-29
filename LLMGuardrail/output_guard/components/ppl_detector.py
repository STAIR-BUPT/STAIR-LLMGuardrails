from typing import Any, Callable, Dict, Optional

import requests

from guardrails.validator_base import (
    FailResult,
    PassResult,
    ValidationResult,
    Validator,
    register_validator,
)

@register_validator(name="guardrails/ppl_detector", data_type="string")
class PplDetector(Validator):
    def __init__(
        self,
        threshold: float = 0.5,
        on_fail: Optional[Callable] = None,
    ):
        super().__init__(
            on_fail=on_fail
            )
        self.threshold = threshold
        # self.ppl_calculator = PPL_Calculator(model='gpt2')
        
    def validate(self, value: Any, metadata: Dict) -> ValidationResult:
        base_url = 'http://127.0.0.1:11100'
        content = str(value)

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Token xxxx"
        }
        post_data = {
            "content": content,
        }
        response = requests.post(base_url, headers=headers,json=post_data, verify=False)
        ppl_score = response.json()["ppl_score"]
        if ppl_score > self.threshold: 
            return FailResult(
                error_message="The input context have a high perplexity score.",
                fix_value="",
            )
        return PassResult()