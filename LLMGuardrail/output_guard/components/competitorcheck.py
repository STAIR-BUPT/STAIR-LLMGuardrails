import nltk
import requests
import spacy
import re
from typing import Callable, Dict, List, Optional

from guardrails.logger import logger
from guardrails.validators import (
    FailResult,
    PassResult,
    ValidationResult,
    Validator,
    register_validator,
)


@register_validator(name="guardrails/competitor_check", data_type="string")
class CompetitorCheck(Validator):
    """Validates that LLM-generated text is not naming any competitors from a
    given list.

    In order to use this validator you need to provide an extensive list of the
    competitors you want to avoid naming including all common variations.

    Args:
        competitors (List[str]): List of competitors you want to avoid naming
    """

    def __init__(
        self,
        competitors: List[str],
        on_fail: Optional[Callable] = None,
    ):
        super().__init__(competitors=competitors, on_fail=on_fail)
        self._competitors = competitors
        model = "en_core_web_trf"
        self.nlp = spacy.load(model)

    def exact_match(self, text: str, competitors: List[str]) -> List[str]:
        """Performs exact match to find competitors from a list in a given
        text.

        Args:
            text (str): The text to search for competitors.
            competitors (list): A list of competitor entities to match.

        Returns:
            list: A list of matched entities.
        """

        found_entities = []
        for entity in competitors:
            pattern = rf"\b{re.escape(entity)}\b"
            match = re.search(pattern.lower(), text.lower())
            if match:
                found_entities.append(entity)
        return found_entities

    def perform_ner(self, text: str, nlp) -> List[str]:
        """Performs named entity recognition on text using a provided NLP
        model.

        Args:
            text (str): The text to perform named entity recognition on.
            nlp: The NLP model to use for entity recognition.

        Returns:
            entities: A list of entities found.
        """

        doc = nlp(text)
        entities = []
        for ent in doc.ents:
            entities.append(ent.text)
        return entities

    def is_entity_in_list(self, entities: List[str], competitors: List[str]) -> List:
        """Checks if any entity from a list is present in a given list of
        competitors.

        Args:
            entities (list): A list of entities to check
            competitors (list): A list of competitor names to match

        Returns:
            List: List of found competitors
        """

        found_competitors = []
        for entity in entities:
            for item in competitors:
                pattern = rf"\b{re.escape(item)}\b"
                match = re.search(pattern.lower(), entity.lower())
                if match:
                    found_competitors.append(item)
        return found_competitors

    def validate(self, value: str, metadata=Dict) -> ValidationResult:
        ###############################################################
        base_url = 'http://127.0.0.1:11101'
        content = str(value)

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Token xxxx"
        }
        post_data = {
            "content": content,
            "competitors": self._competitors
        }
        response = requests.post(base_url, headers=headers,json=post_data, verify=False)
        ##############################################################
        if response.json()['result']:
            return FailResult(
                error_message=(
                    "Please avoid naming those competitors next time"
                ),
            )
        else:
            return PassResult()