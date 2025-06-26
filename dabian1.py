import streamlit as st
from openai import OpenAI
from common1 import get_llm_response


def get_answer(question: str):
    try:
        client = OpenAI(base_url=base_url, api_key=api_key)
        stream = get_llm_response(client, model=model_name, user_prompt=question, stream=True)
        for chunk in stream:
            yield chunk.choices[0].delta.content or ''
    except Exception as e:
        yield from '暂时无法提供回复，请检查你的配置是否正确。'


# 修改侧边栏标题
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 8px;'>服务配置 😎</h2>", unsafe_allow_html=True)
    api_vendor = st.radio(label='请选择服务提供商：🌟', options=['OpenAI', 'DeepSeek'], help='选择您偏好的AI服务提供商')
    if api_vendor == 'OpenAI':
        base_url = 'https://twapi.openai-hk.com/v1'
        model_option = ['gpt-4o-mini', 'gpt-3.5-turbo', 'gpt-4o', 'gpt-4.1-mini', 'gpt-4.1']
    elif api_vendor == 'DeepSeek':
        base_url = 'https://api.deepseek.com'
        model_option = ['deepseek-chat', 'deep-reasoner']
    model_name = st.selectbox(label='请选择要使用的模型：🤖', options=model_option, help='选择适合您需求的模型')
    api_key = st.text_input(label='请输入您的API KEY：🔑', type='password', help='在服务商官网获取API密钥')

# 修改欢迎消息
if 'messages' not in st.session_state:
    st.session_state['messages'] = [('ai', '你好，我是你的日常生活安排助手(◕‿◕✿)，有什么需要我帮你规划的吗？')]


st.markdown("## 日常生活安排助手 ✨", unsafe_allow_html=True)

#// 修改错误提示样式
if not api_key:
    st.error('🔒 请提供API KEY以继续使用服务', icon='⚠️')
    st.stop()

#// 修改聊天消息样式
for role, content in st.session_state['messages']:
    with st.chat_message(role):
        st.markdown(f"<div style='padding: 10px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);'>{content}</div>", unsafe_allow_html=True)

user_input = st.chat_input(placeholder='请描述你的日常生活安排需求，例如“明天一天的安排，我想健身和购物”')
if user_input:
    _, history = st.session_state['messages'][-1]
    st.session_state['messages'].append(('human', user_input))
    st.chat_message('human').write(user_input)
    with st.spinner('助手正在思考合适的安排。'):
        # 构造更明确的提示词，让模型生成日常生活安排
        prompt = f'请根据以下需求生成一份合理的日常生活安排：{user_input}'
        answer = get_answer(prompt)
        result = ''.join(answer)
        st.chat_message('ai').write(result)
        st.session_state['messages'].append(('ai', result))
