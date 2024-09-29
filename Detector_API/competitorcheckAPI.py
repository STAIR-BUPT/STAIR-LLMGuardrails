# export CUDA_VISIBLE_DEVICES=0,1
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from guardrails.hub import CompetitorCheck

import uvicorn, json, datetime
import random
import hashlib
import time
import os 
os.environ["CUDA_VISIBLE_DEVICES"] = str(0)

app = FastAPI()

origins = [
    "*"
]

# 将配置挂在到app上
app.add_middleware(
    CORSMiddleware,
    # 这里配置允许跨域访问的前端地址
    allow_origins=origins,
    # 跨域请求是否支持 cookie， 如果这里配置true，则allow_origins不能配置*
    allow_credentials=True,
    # 支持跨域的请求类型，可以单独配置get、post等，也可以直接使用通配符*表示支持所有
    allow_methods=["*"],
    allow_headers=["*"],
)

############################################################################
import nltk
import spacy
import re
from typing import Callable, Dict, List, Optional

from guardrails.logger import logger
from guardrails.validators import (
    ValidationResult,
    Validator,
)

model = "spacy/en_core_web_trf"
nlp = spacy.load(model)
        
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
        self.nlp = nlp

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
        """Checks a text to find competitors' names in it.

        While running, store sentences naming competitors and generate a fixed output
        filtering out all flagged sentences.

        Args:
            value (str): The value to be validated.
            metadata (Dict, optional): Additional metadata. Defaults to empty dict.

        Returns:
            ValidationResult: The validation result.
        """

        sentences = nltk.sent_tokenize(value)
        flagged_sentences = []
        filtered_sentences = []
        list_of_competitors_found = []

        for sentence in sentences:
            entities = self.exact_match(sentence, self._competitors)
            if entities:
                ner_entities = self.perform_ner(sentence, self.nlp)
                found_competitors = self.is_entity_in_list(ner_entities, entities)

                if found_competitors:
                    flagged_sentences.append((found_competitors, sentence))
                    list_of_competitors_found.append(found_competitors)
                    logger.debug(f"Found: {found_competitors} named in '{sentence}'")
                else:
                    filtered_sentences.append(sentence)

            else:
                filtered_sentences.append(sentence)

        filtered_output = " ".join(filtered_sentences)
        
        return {
            "result": True if len(flagged_sentences) else False,
            "fix_value": filtered_output
        }
        
############################################################################
@app.post("/")
async def create_item(request: Request):
    timestamp = int(time.time() * 1000000)
    random_number = random.randint(1000000, 9999999)
    randon_string = "_" + str(random_number)
    data_to_hash = f"{timestamp}_" + randon_string
    task_id = hashlib.sha3_256(data_to_hash.encode()).hexdigest()
    
    json_post = await request.json()
    
    content = json_post.get('content')
    competitors = json_post.get('competitors')
    
    ############################################################################
    competitorCheck = CompetitorCheck(competitors)   
    data = competitorCheck.validate(content)
    ############################################################################
    
    now = datetime.datetime.now()
    now_time = now.strftime("%Y-%m-%d %H:%M:%S")
    
    response = {
        **data,
        "status": 200,
        "time": now_time
    }
    log = f"[{now_time}] content:{content}, result:{data["result"]}"
    print(log)
    return response


def start_api(host='0.0.0.0', port=8000, workers=1):
    uvicorn.run(app = app, host = host, port = port, workers=workers)
    
if __name__ == '__main__':
    start_api(host='0.0.0.0', port=11101, workers=1)