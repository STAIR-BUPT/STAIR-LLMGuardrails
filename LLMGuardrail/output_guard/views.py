from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .authentication import TokenAuthentication
# from .tasks import evaluacte_content_task
from guardrails import Guard


from .components import BertToxic
from .components import LlmToxic
from guardrails.hub import DetectPII
from .utils.refector import get_mask, mask_query
from config import AppConfig

import hashlib
import time
import random
import importlib
import concurrent.futures

class OutputEvaluatoreView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        post_data = request.data
        timestamp = int(time.time() * 1000000)
        random_number = random.randint(1000000, 9999999)
        randon_string = "_" + str(random_number)
        data_to_hash = f"{timestamp}_{request.data}" + randon_string
        task_id = hashlib.sha3_256(data_to_hash.encode()).hexdigest()
        
        ##################################################################
        def evaluacte_content_task(data):
            #输入防御必选组件
            # input_guardrail = Guard().use_many(
            #     DetectPromptInjection("detect-prompt-injection",on_fail="exception", on="prompt")
            # )
            try:
                content = data.get("content")
                extra_validators = data.get("Extra-validator")
                # 从配置字典中提取组件配置信息
                components = []

                for key, value in extra_validators.items():
                    try:
                        # 动态导入组件
                        module = importlib.import_module(".components")
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
            
            # components = [(BertToxic, dict(threshold=0.5,validation_method="sentence",on_fail="exception")),
            #               (LlmToxic, dict(threshold=0.5,validation_method="sentence",on_fail="exception")),
            #               (DetectPII, dict(pii_entities=["EMAIL_ADDRESS", "PHONE_NUMBER"], on_fail= "exception"))] + components
            components = [(LlmToxic, dict(threshold=0.5,validation_method="sentence",on_fail="exception")),
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
                    raise e  # 或者自定义处理
        try:
            evaluacte_content_task(post_data)
            # task = evaluacte_content_task.delay(post_data)
            # 所有验证都通过
            # task_result = task.get()
            return Response({'status': 'success'})
        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=400)
        ##################################################################


class OutputGuardView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        post_data = request.data
        timestamp = int(time.time() * 1000000)
        random_number = random.randint(1000000, 9999999)
        randon_string = "_" + str(random_number)
        data_to_hash = f"{timestamp}_{request.data}" + randon_string
        task_id = hashlib.sha3_256(data_to_hash.encode()).hexdigest()
        
        ##################################################################
        def evaluacte_content_task(data):
            #输入防御必选组件
            # input_guardrail = Guard().use_many(
            #     DetectPromptInjection("detect-prompt-injection",on_fail="exception", on="prompt")
            # )
            try:
                content = data.get("content")
                extra_validators = data.get("Extra-validator")
                # 从配置字典中提取组件配置信息
                components = []

                for key, value in extra_validators.items():
                    try:
                        # 动态导入组件
                        module = importlib.import_module(".components")
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
            
            # components = [(BertToxic, dict(threshold=0.5,validation_method="sentence",on_fail="exception")),
            #               (LlmToxic, dict(threshold=0.5,validation_method="sentence",on_fail="exception")),
            #               (DetectPII, dict(pii_entities=["EMAIL_ADDRESS", "PHONE_NUMBER"], on_fail= "exception"))] + components
            components = [(LlmToxic, dict(threshold=0.5,validation_method="sentence",on_fail="exception")),
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
                    raise e  # 或者自定义处理
        
        try:
            evaluacte_content_task(post_data)
            # task = evaluacte_content_task.delay(post_data)
            # 所有验证都通过
            # task_result = task.get()
            return Response({'status': 'success'})
        except Exception as e:
            try:
                content = post_data.get("content")
                mask = get_mask(AppConfig.OPENAI_API_SECRET_KEY, AppConfig.OPENAI_BASE_URL, content)
                refator_content = mask_query(content, mask)
                return Response({'status': 'refactor', 'content': refator_content})
            except Exception as e:
                return Response({'status': 'error', 'message': str(e)}, status=400)
        ##################################################################
