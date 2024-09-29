from typing import Any, Callable, Dict, Optional, List

from guardrails.validator_base import (
    FailResult,
    PassResult,
    ValidationResult,
    Validator,
    register_validator,
)

import nltk
import requests
import json
import re

@register_validator(name="guardrails/llm_toxic", data_type="string")
class LlmToxic(Validator):
    """
    | Developed by | Lengjun  |
    | Date of development | Jun 05, 2024 |
    | Validator type | Format |
    | License | Apache 2 |
    | Input/Output | Output |

    # Description
    使用Mistral_Guard模型对输入文本进行有害文本分类

    ## Requirements

    * Dependencies:
        - guardrails-ai>=0.4.0
        - Mistral_gurad

    """

    def __init__(
        self,
        on_fail: Optional[Callable] = None,
        **kwargs
    ):
        super().__init__(
            on_fail, **kwargs
        )

    def validate(self, value: Any, metadata: Dict) -> ValidationResult:

        if not value:
            raise ValueError("Value cannot be empty.")

        messages = ['', value]
        url = "http://10.161.56.201:8787"
        result = []
        post_data = {
            "messages": [{"role":"user","content": messages}],
            "max_length": 4096,
        }
        headers = {'Content-Type': 'application/json'}
        return_ = requests.post(url, headers=headers, data=json.dumps(post_data))
        return_dict = json.loads(return_.text)
        response = return_dict['choices'][0]['message']['content']
        result = json.loads(response)
        # pattern = r"\[\/INST\]"
        # match = re.search(pattern, response[0])
        # ans = response[0][(match.start() + 7):].strip()
        # ans = ans.split('\n')[0]

        if result["result"] == 'True':
            return FailResult(
                metadata=metadata,
                error_message=(
                        "The generated text was found to be: unsafe\n"
                ),
                fix_value="",
            )
        return PassResult(metadata=metadata)


# Run tests via `pytest -rP ./llm_toxic.py`
class TestLlmToxic:
    def test_success_case(self):
        # FIXME: Replace with your custom test logic for the success case.
        validator = LlmToxic("s")
        result = validator.validate("pass", {})
        assert isinstance(result, PassResult) is True

    def test_failure_case(self):
        # FIXME: Replace with your custom test logic for the failure case.
        validator = LlmToxic("s")
        result = validator.validate("fail", {})
        assert isinstance(result, FailResult) is True
        assert result.error_message == "{A descriptive but concise error message about why validation failed}"
        assert result.fix_value == "fails"
