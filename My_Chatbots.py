# 1. 导包
import streamlit as st
from langchain.memory import ConversationBufferMemory
from langchain_community.llms import Tongyi             #lls（大模型语言）：tongyi
from langchain.chains import ConversationChain
from langchain.prompts import ChatPromptTemplate

# 2. 设置做侧边栏
with st.sidebar:
    # 显示文本
    api_key = st.text_input('请输入Tongyi账号的API KEY:', type='password')
    st.markdown("[获取Tongyi账号的API KEY](https://bailian.console.aliyun.com/?spm=5176.29597918.J_SEsSjsNv72yRuRFS2VknO.2.6a2e7b087b88Ea&tab=model#/api-key)")

# 3. 主界面主标题
st.title('通义聊天机器人')

# 4. 会话保持: 用于存储会话记录.
if 'memory' not in st.session_state:
    # 初始化会话记录, memory: 会话记录, messages: 会话记录中的消息列表
    st.session_state['memory'] = ConversationBufferMemory()
    st.session_state['messages'] = [{'role':'ai', 'content':'你好, 我是通义聊天机器人, 有什么可以帮助你的吗?'}]

# 5. 编写1个循环结构, 用于打印会话记录(中的消息列表)
for message in st.session_state.messages:
    # 创建一个消息体, 并且设置消息类型
    with st.chat_message(message['role']):      #设置角色即消息来源
        st.markdown(message['content'])         #打印内容

# 6. 创建1个聊天窗口
prompt = st.chat_input("请输入您要咨询的问题:")

if prompt:  # 如果文本框有数据, 继续往下执行.
    # 7. 显示消息体, 并且设置消息类型为user
    # st.chat_message('user').markdown(prompt)

    # 如果没有API KEY, 直接返回提示.
    st.write(api_key)
    if not api_key:
        st.warning('请输入Tongyi的API KEY!')
        st.stop()
    # 8. 走到这里, 代表: 1. 有API KEY; 2. 有输入文本. 把用户信息显示在主窗体
    st.session_state['messages'].append({'role':'human', 'content':prompt})
    st.chat_message('human').markdown(prompt)
    # 9. 向utils工具类发起请求, 返回响应.
    # 显示一个等待框.
    with st.spinner('AI小助手正在思考中...'):
        content = get_response(prompt, st.session_state['memory'], api_key)

    # 10. 把AI的回复信息, 添加到会话记录中.
    st.session_state['messages'].append({'role':'ai', 'content':content})
    # 11. 把AI的回复信息, 显示在主窗体中.
    st.chat_message('ai').markdown(content)

def get_response(prompt,memory,api_key):
    """
    根据用户录入的提示词, 获取结果(响应体).
    :param prompt: 用户输入的提示词
    :param memory: 记忆体
    :param api_key: API密钥
    :return:
    """
    #3.创建模型对象
    llm = Tongyi(model='qwen-max',dashscope_api_key=api_key)
    #4.创建chains链
    chains = ConversationChain(llm=llm,memory=memory)
    #5.发起请求，获取结果
    response = chains.invoke({'input':prompt})
    #6.response是记忆体，包括之前的会话，本次的会话包含在一个response的key中
    return response['response']

