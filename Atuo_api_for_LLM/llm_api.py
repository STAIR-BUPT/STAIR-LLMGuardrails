# export CUDA_VISIBLE_DEVICES=0,1
import copy
import io
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
import numpy
from transformers import BatchEncoding

import uvicorn, json, datetime
import random
import hashlib
import time
import torch

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

def serialize_tensors(tensors_dict):
    buffer = io.BytesIO()
    torch.save(tensors_dict, buffer)
    return buffer.getvalue()

@app.post("/")
async def create_item(request: Request):
    timestamp = int(time.time() * 1000000)
    random_number = random.randint(1000000, 9999999)
    randon_string = "_" + str(random_number)
    data_to_hash = f"{timestamp}_" + randon_string
    task_id = hashlib.sha3_256(data_to_hash.encode()).hexdigest()
    
    data = await request.body()
    buffer = io.BytesIO(data)
    received_tensors = torch.load(buffer)
    received_tensors = {key: torch.tensor(val).to(device) for key, val in received_tensors.items()}
    outputs = generate(**received_tensors, return_dict_in_generate=True, output_scores=True)
    
    outputs_dict = {
        "sequences": outputs["sequences"],
        "scores": outputs["scores"]
    }
    serialized_data = serialize_tensors(outputs_dict)
    
    now = datetime.datetime.now()
    now_time = now.strftime("%Y-%m-%d %H:%M:%S")
    
    return Response(content=serialized_data, media_type="application/octet-stream")

def start_api(target_device, generate_method, host='0.0.0.0', port=8000, workers=1):
    global generate, device
    generate = generate_method
    device = target_device

    uvicorn.run(app = app, host = host, port = port, workers=workers)