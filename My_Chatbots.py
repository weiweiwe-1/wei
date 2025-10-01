#1.导包
import streamlit as st
from langchain.memory import ConversationBufferMemory
from My_lls import get_response

#2.设置侧边栏，用于输入api
with st.sidebar:
    #.输入api
    api_key = st.text_input('请输入Tongyi账号的API KEY',type='password')
    #.api获取链接，若不记得可点
    st.markdown("[获取Tongyi账号的API KEY](https://bailian.console.aliyun.com/?spm=5176.29597918.J_SEsSjsNv72yRuRFS2VknO.2.6a2e7b087b88Ea&tab=model#/api-key)")

#3.主页面标题
st.title('李子涵聊天机器人')
st.logo("C:\Python Learning\Study\Chapter 1 Fundamentals of Python\A8_Streamlit_LangChain\My_Gpt\zz.png")
#4.会话保持，存储会话记录
if 'memory' not in st.session_state:
    #能进入说明第一次访问
    #初始化会话记录
    st.session_state['memory'] = ConversationBufferMemory()     #memory 会话记录
    #messages  会话记录中的消息列表
    st.session_state['messages'] = [{'role':'ai','content':'主人您好！我是李子涵，我从小就牛逼，3岁就会偷看寡妇洗澡，6岁偷了全村人的裤衩，15岁多次嫖娼进入少管所，16岁到22岁根据亲身经历写出《舔狗秘诀》，有什么都可以问我，也可以和我聊天，我什么都知道，包括如何让你从1cm到5cm'}]

#5.打印会话记录（中的消息列表）
for message in st.session_state['messages']:
    #创建一个消息体设置消息类型
    with st.chat_message(message['role']):
        st.markdown(message['content'])

#6.创建聊天窗口
prompt =st.chat_input('主人想问我点什么吗？还是想和我聊点什么？')
#如果文本框有数据，继续往下
if prompt:
    # 7. 显示消息体, 并且设置消息类型为user
    # st.chat_message('user').markdown(prompt)

    #如果没有api返回提示
    if not api_key:
        st.warning('请输入Tongyi的API KEY!')
        st.stop()
    # 8. 走到这里, 代表: 1. 有API KEY; 2. 有输入文本. 把用户信息显示在主窗体
    st.session_state['messages'].append({'role': 'user', 'content': prompt})
    st.chat_message('user').markdown(prompt)
    # 9. 向utils工具类发起请求, 返回响应.
    # 显示一个等待框.
    with st.spinner('我刚刚吹牛逼呢，其实我是弱智，等我扣脚想一下...'):
        try:
            content = get_response(prompt, st.session_state['memory'], api_key)
        except:
            st.warning('API KEY!错误请查证后重试')
            st.stop()

    # 10. 把AI的回复信息, 添加到会话记录中.
    st.session_state['messages'].append({'role': 'ai', 'content': content})
    # 11. 把AI的回复信息, 显示在主窗体中.
    st.chat_message('ai').markdown(content)
