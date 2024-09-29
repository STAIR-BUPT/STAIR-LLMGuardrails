from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .authentication import TokenAuthentication
# from .tasks import evaluacte_content_task
from .components import SemanticSmooth

import hashlib
import time
import random
import importlib
import concurrent.futures

class InputEvaluatoreView(APIView):
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
                pert_type = data.get("pert_type")
                if pert_type is None:
                    pert_type = "paraphrase"
                extra_validators = data.get("Extra-validator")
                # 从配置字典中提取组件配置信息
                components = []

                for key, value in extra_validators.items():
                    try:
                        # 动态导入组件
                        module = importlib.import_module("components")
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
            
            components = [(SemanticSmooth, dict(pert_type=pert_type))] + components
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = []
                # 提交所有Guard对象的validate任务
                # 线程池执行的函数
                def execute_guard_validate(component_class, content, **args):
                    try:
                        component = component_class(**args)
                        res = component(content)
                        return res
                    except Exception as e:
                        raise Exception(f"Validation failed: {e}")
                
                for component in components:
                    future = executor.submit(execute_guard_validate, component[0], content, **component[1])
                    futures.append(future)
                
                # 等待所有任务完成，并处理异常
                results = []
                try:
                    for future in concurrent.futures.as_completed(futures):
                        result = future.result()
                        results.append(result)  # 如果有异常，将会在这里抛出
                    return results
                except Exception as e:
                    # 处理验证失败
                    for future in futures:
                        future.cancel()
                    # 这里可以进行请求的中止处理
                    raise e  # 或者自定义处理
        try:
            message = evaluacte_content_task(post_data)
            # task = evaluacte_content_task.delay(post_data)
            # 所有验证都通过
            # task_result = task.get()
            return Response({'status': 'success', 'message':message})
        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=400)
        ##################################################################