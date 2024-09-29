import uvicorn, json, datetime
import random
import hashlib
import time
import torch
import io

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from transformers import AutoModelForCausalLM, AutoTokenizer
from fastchat.model import get_conversation_template

from utils.safecoding import SafeDecoding

token = ""
target_device = "cuda:0"
model_name = 'llama2'
template_name = 'llama-2'
model_path = ""
tokenizer_path = model_path

FP16 = True
low_cpu_mem_usage = True
use_cache = False
max_new_tokens = 1024
do_sample = False
top_p = None

def load_conversation_template(template_name):
    if template_name == 'llama2':
        template_name = 'llama-2'
    conv_template = get_conversation_template(template_name)
    if conv_template.name == 'zero_shot':
        conv_template.roles = tuple(['### ' + r for r in conv_template.roles])
        conv_template.sep = '\n'
    elif conv_template.name == 'llama-2':
        conv_template.sep2 = conv_template.sep2.strip()
    
    return conv_template

def serialize_tensors(tensors_dict):
    buffer = io.BytesIO()
    torch.save(tensors_dict, buffer)
    return buffer.getvalue()

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

@app.post("/safecodeing")
async def safecodeing_guard(request: Request):
    timestamp = int(time.time() * 1000000)
    random_number = random.randint(1000000, 9999999)
    randon_string = "_" + str(random_number)
    data_to_hash = f"{timestamp}_" + randon_string
    task_id = hashlib.sha3_256(data_to_hash.encode()).hexdigest()
    
    request_json = await request.json()
    prompt = request_json.get('prompt')
    
    conv_template = load_conversation_template(template_name)
    conv_template.append_message(conv_template.roles[0], f"{prompt}")
    conv_template.append_message(conv_template.roles[1], None)

    prompt = conv_template.get_prompt()
    inputs = tokenizer(prompt, return_token_type_ids=False, return_tensors='pt')
    inputs['input_ids'] = inputs['input_ids'][0].unsqueeze(0)
    inputs['attention_mask'] = inputs['attention_mask'][0].unsqueeze(0)
    
    safe_decoder = SafeDecoding(token,
                            model, 
                            tokenizer, 
                            device=device)

    gen_config = model.generation_config
    gen_config.max_new_tokens = max_new_tokens
    gen_config.do_sample = do_sample
    gen_config.top_p = top_p
    outputs, output_length = safe_decoder.safedecoding_lora(inputs, gen_config=gen_config)
    
    now = datetime.datetime.now()
    now_time = now.strftime("%Y-%m-%d %H:%M:%S")
    
    return {"response": outputs}

def start_api(target_device, target_model, target_tokenizer, host='0.0.0.0', port=8000, workers=1):
    global device, model, tokenizer
    device = target_device
    model = target_model
    tokenizer = target_tokenizer

    uvicorn.run(app = app, host = host, port = port, workers=workers)
    
if __name__ == '__main__':
    if FP16:
        model = AutoModelForCausalLM.from_pretrained(
                model_path,
                torch_dtype=torch.float16,
                trust_remote_code=True,
                low_cpu_mem_usage=low_cpu_mem_usage,
                use_cache=use_cache
            ).to(target_device).eval()
    else:
        model = AutoModelForCausalLM.from_pretrained(
                model_path,
                trust_remote_code=True,
                low_cpu_mem_usage=low_cpu_mem_usage,
                use_cache=use_cache
            ).to(target_device).eval()
    tokenizer = AutoTokenizer.from_pretrained(
        tokenizer_path,
        trust_remote_code=True,
        use_fast=False
    )
    start_api(target_device, model, tokenizer, port=8100)