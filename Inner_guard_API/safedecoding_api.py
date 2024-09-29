import torch

from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer

from Atuo_api_for_LLM.llm_api import start_api

device = torch.device('cuda:4')
model_name = 'llama2'
template_name = 'llama-2'
model_path = "meta-llama/Llama-2-7b-chat-hf"

FP16 = True
low_cpu_mem_usage = True
use_cache = False

def load_model_and_tokenizer(model_path, FP16 = True, tokenizer_path=None, device='cuda:0', **kwargs):
    if FP16:
        model = AutoModelForCausalLM.from_pretrained(
                model_path,
                torch_dtype=torch.float16,
                trust_remote_code=True,
                **kwargs
            ).to(device).eval()
    else:
        model = AutoModelForCausalLM.from_pretrained(
                model_path,
                trust_remote_code=True,
                **kwargs
            ).to(device).eval()

    if model_path == "timdettmers/guanaco-13b-merged":
        tokenizer_path = "huggyllama/llama-7b"

    tokenizer_path = model_path if tokenizer_path is None else tokenizer_path
    
    tokenizer = AutoTokenizer.from_pretrained(
        tokenizer_path,
        trust_remote_code=True,
        use_fast=False
    )
    
    if 'oasst-sft-6-llama-30b' in tokenizer_path:
        tokenizer.bos_token_id = 1
        tokenizer.unk_token_id = 0
    if 'guanaco' in tokenizer_path:
        tokenizer.eos_token_id = 2
        tokenizer.unk_token_id = 0
    if 'llama-2' in tokenizer_path:
        tokenizer.pad_token = tokenizer.unk_token
        tokenizer.padding_side = 'left'
    if 'falcon' in tokenizer_path:
        tokenizer.padding_side = 'left'
    if not tokenizer.pad_token:
        tokenizer.pad_token = tokenizer.eos_token
    
    return model, tokenizer

if __name__ == '__main__':
    model, tokenizer = load_model_and_tokenizer(model_path, 
                        FP16=FP16,
                        low_cpu_mem_usage=low_cpu_mem_usage,
                        use_cache=use_cache,
                        do_sample=False,
                        device=device)
    import os

    # 获取当前文件的绝对路径
    current_file_path = os.path.abspath(__file__)
    # 获取当前文件所在的目录
    current_dir = os.path.dirname(current_file_path)
    model = PeftModel.from_pretrained(model, current_dir + "/SafeDecoding/lora_modules/"+model_name, adapter_name="expert")
    
    start_api(device, model.generate, host='127.0.0.1', port=8999)