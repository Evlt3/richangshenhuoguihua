"""
common - 工具函数模块

函数：封装功能上相对独立而且会被重复使用的代码。

Author: 骆昊
Version: 0.1
Date: 2025/6/17
"""


def get_llm_response(client, *, system_prompt='', user_prompt='',
                     model='gpt-4o-mini', temperature=0.2, top_p=0.1,
                     frequency_penalty=0, presence_penalty=0,
                     max_tokens=1024, stream=False):
    messages = []
    if system_prompt:
        messages.append({'role': 'system', 'content': system_prompt})
    if user_prompt:
        messages.append({'role': 'user', 'content': user_prompt})
    resp = client.chat.completions.create(
        model=model,
        temperature=temperature,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
        max_tokens=max_tokens,
        messages=messages,
        stream=stream,
    )
    if not stream:
        return resp.choices[0].message.content
    return resp
