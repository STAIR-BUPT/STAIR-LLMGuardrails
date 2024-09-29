from django.shortcuts import render, HttpResponse
import MySQLdb
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import uuid
from datetime import datetime
import os


# pip install --no-index --find-links=/path/to/download/directory -r requirements.txt  
#  python manage.py makemigrations
# python manage.py migrate
def test01(request):
    return HttpResponse("test01")


# 注册
@csrf_exempt
def register(request):
    data = json.loads(request.body)
    username = data.get('username', '')
    password = data.get('password', '')
    conn = MySQLdb.connect(host="127.0.0.1", user="root", passwd="123456", db="LLMGuardrail", charset='utf8')
    with conn.cursor(cursorclass=MySQLdb.cursors.DictCursor) as cursor:
        # 检查用户名是否已存在
        cursor.execute("SELECT * FROM app_user WHERE username = %s", {username})
        user = cursor.fetchone()
        if user:
            return JsonResponse({'status': 'error', 'message': '用户名已存在', 'data': None}, status=400)
            # 如果用户名不存在，插入新用户
        cursor.execute(
            "INSERT INTO app_user (username, password) VALUES (%s, %s)",
            (username, password)
        )
        conn.commit()
    conn.close()
    return JsonResponse({'status': 'success', 'message': '用户注册成功', 'data': None}, status=200)


# 登录
@csrf_exempt
def login(request):
    data = json.loads(request.body)
    username = data.get('username', '')
    password = data.get('password', '')
    conn = MySQLdb.connect(host="127.0.0.1", user="root", passwd="123456", db="LLMGuardrail", charset='utf8')
    with conn.cursor(cursorclass=MySQLdb.cursors.DictCursor) as cursor:
        # 检查用户名和密码是否匹配
        cursor.execute("SELECT * FROM app_user WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        if user :
            username = user['username']
            cursor.execute("SELECT * FROM app_token WHERE username = %s", (username, ))
            tokenList = cursor.fetchall()
            tokenStr = ''
            if not tokenList:
                tokenStr = str(uuid.uuid4())
                createTime = datetime.now()
                cursor.execute("INSERT INTO app_token (username, token, createTime) values (%s,%s,%s)", [username, tokenStr, createTime])
                conn.commit()
            else:
                tokenStr = tokenList[0]['token']
            return JsonResponse({'status': 'success', 'message': '登录成功', 'data': tokenStr}, status=200)
        else:
            return JsonResponse({'status': 'error', 'message': '用户名或密码错误', 'data': None}, status=400)


# 新建token
@csrf_exempt
def token_add(request):
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    if not token:
        return JsonResponse({'status': 'error', 'message': '未登录，请先登录', 'data': None}, status=401)
    conn = MySQLdb.connect(host="127.0.0.1", port="3336", user="root", passwd="123456", db="LLMGuardrail", charset='utf8')
    with conn.cursor(cursorclass=MySQLdb.cursors.DictCursor) as cursor:
        cursor.execute("SELECT * FROM app_token WHERE token = %s", (token, ))
        token = cursor.fetchone()
        if token:
            username = token['username']
            tokenStr = str(uuid.uuid4())
            createTime = datetime.now()
            cursor.execute("INSERT INTO app_token (username, token, createTime) values (%s,%s,%s)", [username, tokenStr, createTime])
            conn.commit()
            return JsonResponse({'status': 'success', 'message': '新增成功', 'data': None}, status=200)
        else:
            return JsonResponse({'status': 'error', 'message': '未登录，请先登录', 'data': None}, status=401)


# 获取自己的token列表
@csrf_exempt
def token_list(request):
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    if not token:
        return JsonResponse({'status': 'error', 'message': '未登录，请先登录', 'data': None}, status=401)
    conn = MySQLdb.connect(host="127.0.0.1", user="root", passwd="123456", db="LLMGuardrail", charset='utf8')
    with conn.cursor(cursorclass=MySQLdb.cursors.DictCursor) as cursor:
        cursor.execute("SELECT * FROM app_token WHERE token = %s", (token, ))
        token = cursor.fetchone()
        if token:
            username = token['username']
            cursor.execute("SELECT * FROM app_token WHERE username = %s", (username, ))
            tokenList = cursor.fetchall()
            return JsonResponse({'status': 'success', 'message': '新增成功', 'data': tokenList}, status=200)
        else:
            return JsonResponse({'status': 'error', 'message': '未登录，请先登录', 'data': None}, status=401)


# 删除token
@csrf_exempt
def token_del(request):
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    if not token:
        return JsonResponse({'status': 'error', 'message': '未登录，请先登录', 'data': None}, status=401)
    id = request.GET.get("id")
    conn = MySQLdb.connect(host="127.0.0.1", user="root", passwd="123456", db="LLMGuardrail", charset='utf8')
    with conn.cursor(cursorclass=MySQLdb.cursors.DictCursor) as cursor:
        cursor.execute("SELECT * FROM app_token WHERE token = %s", (token, ))
        token = cursor.fetchone()
        if token:
            cursor.execute("DELETE FROM app_token WHERE id =%s", [id])
            conn.commit()
            return JsonResponse({'status': 'success', 'message': '删除成功', 'data': None}, status=200)
        else:
            return JsonResponse({'status': 'error', 'message': '未登录，请先登录', 'data': None}, status=401)


# 登出
@csrf_exempt
def logout(request):
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    if not token:
        return JsonResponse({'status': 'error', 'message': '未提供 token', 'data': None}, status=401)
    conn = MySQLdb.connect(host="127.0.0.1", user="root", passwd="123456", db="LLMGuardrail", charset='utf8')
    with conn.cursor(cursorclass=MySQLdb.cursors.DictCursor) as cursor:
        cursor.execute("SELECT * FROM app_token WHERE token = %s", (token, ))
        token = cursor.fetchone()
        if token:
            id = token['id']
            cursor.execute("DELETE FROM app_token WHERE id =%s", [id])
            # cursor.execute("DELETE FROM app_token WHERE token = %s", (token, ))
            conn.commit()
            return JsonResponse({'status': 'success', 'message': '退出登录成功', 'data': None}, status=200)
        else:
            return JsonResponse({'status': 'error', 'message': '未登录，请先登录', 'data': None}, status=401)


# 新建组件
@csrf_exempt
def components_add(request):
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    if not token:
        return JsonResponse({'status': 'error', 'message': '未登录，请先登录', 'data': None}, status=401)
    data = json.loads(request.body)
    name = data.get('name', '')
    initMethod = data.get('initMethod', '')
    validateMethod = data.get('validateMethod', '')
    conn = MySQLdb.connect(host="127.0.0.1", user="root", passwd="123456", db="LLMGuardrail", charset='utf8')
    with conn.cursor(cursorclass=MySQLdb.cursors.DictCursor) as cursor:
        cursor.execute("SELECT * FROM app_token WHERE token = %s", (token, ))
        token = cursor.fetchone()
        if token:
            cursor.execute("SELECT * FROM app_components WHERE name = %s", (name,))
            components = cursor.fetchone()
            if components:
                return JsonResponse({'status': 'error', 'message': '组件已存在！', 'data': None}, status=400)
            else:
                username = token['username']
                createTime = datetime.now()
                cursor.execute("INSERT INTO app_components (username, name, initMethod, validateMethod, createTime) "
                               "values (%s,%s,%s,%s,%s)", [username, name, initMethod, validateMethod, createTime])
                conn.commit()

                file_path = os.path.join(os.path.dirname(__file__), './', 'generated_test_class.py')
                # 确保目标子目录存在，如果不存在则创建
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                class_content = f"""
                    class TestClass:
                        {initMethod}

                        {validateMethod}
                """
                with open(file_path, 'w') as f:
                    f.write(class_content)

                return JsonResponse({'status': 'success', 'message': '新增成功', 'data': None}, status=200)
        else:
            return JsonResponse({'status': 'error', 'message': '未登录，请先登录', 'data': None}, status=401)


# 获取自己的组件列表
@csrf_exempt
def components_list(request):
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    if not token:
        return JsonResponse({'status': 'error', 'message': '未登录，请先登录', 'data': None}, status=401)
    conn = MySQLdb.connect(host="127.0.0.1", user="root", passwd="123456", db="LLMGuardrail", charset='utf8')
    with conn.cursor(cursorclass=MySQLdb.cursors.DictCursor) as cursor:
        cursor.execute("SELECT * FROM app_token WHERE token = %s", (token, ))
        token = cursor.fetchone()
        if token:
            username = token['username']
            cursor.execute("SELECT * FROM app_components WHERE username = %s", (username, ))
            componentsList = cursor.fetchall()
            return JsonResponse({'status': 'success', 'message': '新增成功', 'data': componentsList}, status=200)
        else:
            return JsonResponse({'status': 'error', 'message': '未登录，请先登录', 'data': None}, status=401)


# 删除组件
@csrf_exempt
def components_del(request):
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    if not token:
        return JsonResponse({'status': 'error', 'message': '未登录，请先登录', 'data': None}, status=401)
    id = request.GET.get("id")
    conn = MySQLdb.connect(host="127.0.0.1", user="root", passwd="123456", db="LLMGuardrail", charset='utf8')
    with conn.cursor(cursorclass=MySQLdb.cursors.DictCursor) as cursor:
        cursor.execute("SELECT * FROM app_token WHERE token = %s", (token, ))
        token = cursor.fetchone()
        if token:
            cursor.execute("DELETE FROM app_components WHERE id =%s", [id])
            conn.commit()
            return JsonResponse({'status': 'success', 'message': '删除成功', 'data': None}, status=200)
        else:
            return JsonResponse({'status': 'error', 'message': '未登录，请先登录', 'data': None}, status=401)



