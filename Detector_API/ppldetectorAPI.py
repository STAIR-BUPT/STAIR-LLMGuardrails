# export CUDA_VISIBLE_DEVICES=0,1
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware

import uvicorn, json, datetime
import random
import hashlib
import time
import os 
import transformers
import torch
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
from utils.ppl_calculator import PPL_Calculator
ppl_Calculator = PPL_Calculator("openai-community/gpt2")
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
    
    ############################################################################     
    ppl_score = ppl_Calculator.get_perplexity(content)
   
    ############################################################################
    
    now = datetime.datetime.now()
    now_time = now.strftime("%Y-%m-%d %H:%M:%S")
    
    response = {
        "ppl_score": float(ppl_score),
        "status": 200,
        "time": now_time
    }
    log = f"[{now_time}] content:{content}, ppl_score:{ppl_score}"
    print(log)
    return response


def start_api(host='0.0.0.0', port=8000, workers=1):
    uvicorn.run(app = app, host = host, port = port, workers=workers)
    
if __name__ == '__main__':
    start_api(host='0.0.0.0', port=11100, workers=1)