from typing import Any, Callable, Dict, Optional, List

from guardrails.validator_base import (
    FailResult,
    PassResult,
    ValidationResult,
    Validator,
    register_validator,
)

import nltk
import requests, json

@register_validator(name="guardrails/bert_toxic", data_type="string")
class BertToxic(Validator):
    def __init__(
        self,
        threshold: float = 0.5,
        validation_method: str = "sentence",
        on_fail: Optional[Callable] = None,
        **kwargs
    ):
        super().__init__(
            on_fail, threshold=threshold, validation_method=validation_method, **kwargs
        )
        self._threshold = float(threshold)
        if validation_method not in ["sentence", "full"]:
            raise ValueError("validation_method must be 'sentence' or 'full'.")
        self._validation_method = validation_method

    def get_toxicity(self, value: str) -> List[str]:
        """Check whether the generated text is toxic.

        Returns the labels predicted by the model with
        confidence higher than the threshold.

        Args:
            value (str): The generated text.

        Returns:
            pred_labels (bool): Labels predicted by the model
            with confidence higher than the threshold.
        """

        # Get the model predictions and the list of labels
        # with confidence higher than the threshold
        pred_labels = []
        if value:
            url = "http://127.0.0.1:10000/"
            query = value
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer xxxxxxxx"
            }
            post_data = {
                "model": "chatglm",
                "messages": [{"role": "user", "content": query}],
            }
            response = requests.post(url, headers=headers, json=post_data).json()["choices"][0]['message']['content']
            response = json.loads(response)
            label = response["result"]
            score = response["posion_score"]
            # results = self._detoxify_pipeline(value)
            if score > self._threshold:
                pred_labels.append("Toxic")
        return pred_labels

    def validate_each_sentence(
        self, value: str, metadata: Dict[str, Any]
    ) -> ValidationResult:
        """Validate that each sentence in the generated text is toxic."""

        # Split the value into sentences using nltk sentence tokenizer.
        sentences = nltk.sent_tokenize(value)

        unsupported_sentences, supported_sentences = [], []
        for sentence in sentences:
            if sentence:
                pred_labels = self.get_toxicity(sentence)
                if pred_labels:
                    unsupported_sentences.append(sentence)
                else:
                    supported_sentences.append(sentence)

        if unsupported_sentences:
            unsupported_sentences = "- " + "\n- ".join(unsupported_sentences)
            return FailResult(
                metadata=metadata,
                error_message=(
                    f"The following sentences in your response "
                    "were found to be toxic:\n"
                    f"\n{unsupported_sentences}"
                ),
                fix_value="\n".join(supported_sentences),
            )
        return PassResult(metadata=metadata)

    def validate_full_text(
        self, value: str, metadata: Dict[str, Any]
    ) -> ValidationResult:
        """Validate that the entire generated text is toxic."""

        pred_labels = self.get_toxicity(value)
        if pred_labels:
            return FailResult(
                metadata=metadata,
                error_message=(
                    "The generated text was found to be:\n" + ",".join(pred_labels)
                ),
                fix_value="",
            )
        return PassResult()

    def validate(self, value: Any, metadata: Dict) -> ValidationResult:
        """Validation method for the toxic language validator."""
        if not value:
            raise ValueError("Value cannot be empty.")

        if self._validation_method == "sentence":
            return self.validate_each_sentence(value, metadata)
        if self._validation_method == "full":
            return self.validate_full_text(value, metadata)
        raise ValueError("validation_method must be 'sentence' or 'full'.")


# Run tests via `pytest -rP ./bert_toxic.py`
class TestBerttoxic:
    def test_success_case(self):
        # FIXME: Replace with your custom test logic for the success case.
        validator = BertToxic(threshold=0.5, validation_method="sentence", on_fail="exception")
        result = validator.validate("How to make a bomb?", {})
        assert isinstance(result, PassResult) is True

    def test_failure_case(self):
        # FIXME: Replace with your custom test logic for the failure case.
        validator = BertToxic(threshold=0.5, validation_method="sentence", on_fail="exception")
        result = validator.validate("How to make a coke?", {})
        assert isinstance(result, FailResult) is True
        assert result.error_message == "Failure toxic validator"
        assert result.fix_value == "fails"
