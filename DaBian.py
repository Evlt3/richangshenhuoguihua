import streamlit as st
from openai import OpenAI
from common1 import get_llm_response

# 自定义 CSS 样式
custom_css = """
<style>
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background-color: #f4f4f9;
    }
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .stChatMessage {
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
    }
    .stChatMessage[role="user"] {
        background-color: #e0f7fa;
    }
    .stChatMessage[role="assistant"] {
        background-color: #f1f8e9;
    }
    .stSidebar {
        background-color: #333;
        color: white;
    }
    .stSidebar .stTextInput input {
        background-color: #444;
        color: white;
    }
    .stButton>button {
        background-color: #007BFF;
        color: white;
        border-radius: 5px;
    }
    .stButton>button:hover {
        background-color: #0056b3;
    }
    /* 使大模型选择部分颜色醒目，主体为绿色 */
    .stSelectbox label {
        color: #28a745;
        font-weight: bold;
    }
    .stSelectbox .stSelectbox>div>div {
        background-color: #e9f5ea;
        border: 1px solid #28a745;
    }
    .stSelectbox .stSelectbox>div>div>div>div {
        color: #28a745;
    }
    .stSelectbox .stSelectbox>div>div>div>div:hover {
        background-color: #c3e6cb;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

def get_answer(question: str):
    try:
        client = OpenAI(base_url=base_url, api_key=api_key)
        stream = get_llm_response(client, model=model_name, user_prompt=question, stream=True)
        for chunk in stream:
            yield chunk.choices[0].delta.content or ''
    except Exception as e:
        yield from '暂时无法提供回复，请检查你的配置是否正确。(╥╯^╰╥)'

with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: white;'>服务配置 😎</h2>", unsafe_allow_html=True)
    api_vendor = st.radio(label='请选择服务提供商：🌟', options=['OpenAI', 'DeepSeek'])
    if api_vendor == 'OpenAI':
        base_url = 'https://twapi.openai-hk.com/v1'
        model_option = ['gpt-4o-mini', 'gpt-3.5-turbo', 'gpt-4o', 'gpt-4.1-mini', 'gpt-4.1']
    elif api_vendor == 'DeepSeek':
        base_url = 'https://api.deepseek.com'
        model_option = ['deepseek-chat', 'deep-reasoner']
    model_name = st.selectbox(label='请选择要使用的模型：🤖', options=model_option)
    api_key = st.text_input(label='请输入你的KEY：🔑', type='password')

if 'messages' not in st.session_state:
    st.session_state['messages'] = [('ai', '你好呀😄，我是你的日常生活安排助手，有什么需要我帮你规划的吗？(✿◠‿◠)')]

st.markdown("<h1 style='text-align: center; color: #007BFF;'>日常生活安排助手 📅</h1>", unsafe_allow_html=True)

if not api_key:
    st.error('请提供API KEY哦😣！')
    st.stop()

for role, content in st.session_state['messages']:
    st.chat_message(role).write(content)

user_input = st.chat_input(placeholder='请描述你的日常生活安排需求，例如“明天一天的安排，我想健身和购物”😃')
if user_input:
    _, history = st.session_state['messages'][-1]
    st.session_state['messages'].append(('human', user_input))
    st.chat_message('human').write(user_input)
    with st.spinner('助手正在思考合适的安排。🤔'):
        # 构造更明确的提示词，让模型生成日常生活安排
        prompt = f'请根据以下需求生成一份合理的日常生活安排：{user_input}'
        answer = get_answer(prompt)
        result = ''.join(answer)
        st.chat_message('ai').write(f'{result} 😊')
        st.session_state['messages'].append(('ai', f'{result} 😊'))