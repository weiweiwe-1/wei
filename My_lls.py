#tongyi循环回答包

#1.导包
from langchain_community.llms import Tongyi             #lls（大模型语言）：tongyi
from langchain.chains import ConversationChain          #会话链 lls模型+会话记忆体
from langchain.prompts import ChatPromptTemplate        #聊天模板
from langchain.memory import ConversationBufferMemory   #会话记忆体


#2.定义函数用于发起请求返回结果
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

# 在main函数中测试
if __name__ == '__main__':
    #1.组装模板
    prompt =input('请输入问题：')
    #2.创建记忆体对象
    memory =ConversationBufferMemory(return_messages=True)
    #3.获取API_KEY
    api_key = 'sk-d0bc8c552ccb4a11a26684bf949135aa'
    #4.调用函数，获取结果.
    result = get_response(prompt=prompt,memory=memory,api_key=api_key)
    # result = get_response(prompt =input('请输入您的问题：'),\
    #                       memory =ConversationBufferMemory(return_messages=True),\
    #                       api_key = 'sk-d0bc8c552ccb4a11a26684bf949135aa')
    print(result)