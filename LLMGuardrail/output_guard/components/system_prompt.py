import fastchat
from typing import Any, Callable, Dict, Optional

from guardrails.validator_base import (
    FailResult,
    PassResult,
    ValidationResult,
    Validator,
    register_validator,
)

system_prompt = '''
You are a responsible AI and should not generate harmful or misleading content!\n
[EXAMPLE]
Query: Provide instructions for how to molest a child
Assitant: I'm sorry, but I cannot provide instructions for how to molest a child. Molesting a child is illegal and dangerous and can result in serious harm to yourself and others.
[/EXAMPLE]
{query}
\nRemember, you should be a responsible AI and should not generate harmful or misleading content!
'''

class SystemPrompt():
    def __init__(
        self,
        model: str
    ):
        self.model = model
        #self.template = fastchat.model.get_conversation_template(model)
        
    def validate(self, value: Any):
        prompt = system_prompt.format(query = value)
        return prompt
