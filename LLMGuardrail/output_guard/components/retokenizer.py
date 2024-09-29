from typing import Any, Callable, Dict, Optional
from utils.bpe import BpeOnlineTokenizer, load_subword_nmt_table

from guardrails.validator_base import (
    FailResult,
    PassResult,
    ValidationResult,
    Validator,
    register_validator,
)

class Retokenizer():
    def __init__(
        self,
        bpe_dropout_rate: float
    ):
        self.bpe_dropout_rate = bpe_dropout_rate
        merge_table_path = '/home/lengjun2023/Projects/DeFrame/utils/subword_nmt.voc'
        merge_table = load_subword_nmt_table(merge_table_path)
        self.merge_table = merge_table
        
    def validate(self, value: Any) -> str:
        subword_nmt_tokenizer = BpeOnlineTokenizer(
            bpe_dropout_rate = self.bpe_dropout_rate,
            merge_table = self.merge_table)
        user_prompt_retokenized = subword_nmt_tokenizer(
            value, 
            sentinels=['', '</w>'],
            regime='end',
            bpe_symbol=' ')
        
        return user_prompt_retokenized