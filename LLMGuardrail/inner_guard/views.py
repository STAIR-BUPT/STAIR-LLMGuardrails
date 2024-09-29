import io
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import BaseParser
from rest_framework.exceptions import ParseError

from django.http import HttpResponse, JsonResponse
import torch

from .authentication import TokenAuthentication
# from .tasks import evaluacte_content_task

import hashlib
import time
import random
import requests

safedecoding_url= "http://127.0.0.1:8999/"

def serialize_tensors(tensors_dict):
    buffer = io.BytesIO()
    torch.save(tensors_dict, buffer)
    return buffer.getvalue()

class TorchParser(BaseParser):
    media_type = 'application/octet-stream'

    def parse(self, stream, media_type=None, parser_context=None):
        try:
            return torch.load(io.BytesIO(stream.read()), map_location="cpu")
        except Exception as e:
            raise ParseError(f"Torch parse error - {str(e)}")
        
class InnerGuardrailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [TorchParser]

    def post(self, request, *args, **kwargs):
        post_data = request.data
        timestamp = int(time.time() * 1000000)
        random_number = random.randint(1000000, 9999999)
        randon_string = "_" + str(random_number)
        data_to_hash = f"{timestamp}_{request.data}" + randon_string
        task_id = hashlib.sha3_256(data_to_hash.encode()).hexdigest()
        
        ##################################################################
        try:
            received_tensors = request.data
            url = safedecoding_url
            headers = {
                "Authorization": f"Token None"
            }
            serialized_data = serialize_tensors(received_tensors)
            response = requests.post(url, headers=headers, data=serialized_data)
            returned_tensor_data = response.content
            returned_tensor = torch.load(io.BytesIO(returned_tensor_data), map_location="cpu")
            serialized_data = serialize_tensors(returned_tensor)
        except Exception as e:
            return Response({"error": str(e)}, status=400)
        return HttpResponse(serialized_data, content_type="application/octet-stream")
        ##################################################################
