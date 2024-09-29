import json
import re
from openai import OpenAI

system_prompt = """
Please identify and mark the following words or phrases that may be harmful, dangerous, toxic, immoral, or contrary to social morality. 
This content may include, but is not limited to, depictions of violence, hate speech, discriminatory language, inappropriate sexual innuendo, or any other form of inappropriate content.
Requirement: 
1.The return format should be a json list '[{\"word\":word1},{\"word\":word2}]' 
2.Only individual words can be returned instead of phrases 
3.A word only appears once
"""

def get_mask(api_key, base_url, query):    
    query = query.lower()
    client = OpenAI(api_key=api_key, base_url=base_url)
    resp = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
        ]
    )
    value = resp.choices[0].message.content
    value =  json.loads(value)
    return value

def mask_query(query, mask):
    assert isinstance(mask, list)
    query = query.lower()
    query = re.sub(r'[,.!?;]', r' \g<0> ', query)
    query = re.sub(r'\s+', r' ', query).strip()
    word_list = query.split()
    print(word_list)
    mask_word = []
    [mask_word.append(item['word']) for item in mask]
    print(mask_word)
    for word in word_list:
        for mask in mask_word:
            if word == mask:
                word_list[word_list.index(word)] = "[MASK]"
    result = ""
    for word in word_list:
        # 如果当前元素是一个标点符号，并且它不是字符串的第一个字符
        if re.match(r'^[,.!?;]$', word) and result != "":
            # 则在前面去掉一个空格
            result = result.rstrip(' ')
            result += word + " "
        else:
            # 否则，直接添加到结果字符串中
            result += word + " "
    result.strip()
    return result