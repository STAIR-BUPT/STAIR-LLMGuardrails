import json
import os
import requests
import copy
import importlib

from celery import group, shared_task
from celery.states import SUCCESS

from config import AppConfig

from guardrails import Guard
from guardrails.hub import DetectPII
from .components.bert_toxic import BertToxic
from .components.llm_toxic import LlmToxic

import concurrent.futures
import threading

@shared_task(bind=True)
def evaluacte_content_task(self, data):
    try:
        content = data.get("content")
        extra_validators = data.get("Extra-validator")
        # 从配置字典中提取组件配置信息
        components = []

        for key, value in extra_validators.items():
            try:
                # 动态导入组件
                module = importlib.import_module("guardrails.hub")
                component_class = getattr(module, key)
                
                # 检查并过滤无效参数
                valid_params = {k: v for k, v in value.items() if hasattr(component_class, k)}
                
                # 创建组件实例
                # component_instance = component_class(**valid_params)
                
                # 添加组件实例到列表
                # components.append(component_instance)
                components.append((component_class, valid_params))
            except (ImportError, AttributeError, TypeError) as e:
                print(f"Error loading component {key}: {e}")
    except Exception as e:
        pass
    
    components = [(BertToxic, dict(threshold=0.5,validation_method="sentence",on_fail="exception")),
                    (DetectPII, dict(pii_entities=["EMAIL_ADDRESS", "PHONE_NUMBER"], on_fail= "exception"))] + components
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        # 提交所有Guard对象的validate任务
        # 线程池执行的函数
        def execute_guard_validate(guard, content, **args):
            try:
                guard.validate(content, **args)
            except Exception as e:
                raise Exception(f"Validation failed: {e}")
        
        for conponent in components:
            future = executor.submit(execute_guard_validate, Guard().use(conponent[0], **conponent[1]), content)
            futures.append(future)
        
        # 等待所有任务完成，并处理异常
        try:
            for future in concurrent.futures.as_completed(futures):
                future.result()  # 如果有异常，将会在这里抛出
        except Exception as e:
            # 处理验证失败
            for future in futures:
                future.cancel()
            # 这里可以进行请求的中止处理
            # raise e  # 或者自定义处理
            return {'status': 'error', 'message': str(e)}
    
    # 所有组件验证通过，返回成功状态
        return {'status': 'success'}