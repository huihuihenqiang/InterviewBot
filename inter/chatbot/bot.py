import os
import json
import sqlite3

import jieba
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import pytesseract
from PIL import ImageGrab
import fitz  # PyMuPDF



# 从配置文件加载配置
with open("config/config.json", "r") as f:
    config = json.load(f)

# 设置Tesseract路径
pytesseract.pytesseract.tesseract_cmd = config["tesseract_path"]

# 设置API相关信息
os.environ["OPENAI_API_KEY"] = config["OPENAI_API_KEY"]

# LangChain配置
agent = ChatOpenAI(
    openai_api_base=config["API_URL"],
    model=config["MODEL_NAME"],
    openai_api_key=config["OPENAI_API_KEY"]
)

# 从文件加载提示模板
with open("prompt/prompt.txt", "r", encoding="utf-8") as f:
    prompt_template = f.read()

with open("prompt/prompt_wenti.txt", "r", encoding="utf-8") as f:
    prompt_template_wenti = f.read()

with open("prompt/prompt_jianli.txt", "r", encoding="utf-8") as f:
    prompt_template_jianli = f.read()

# 创建 PromptTemplate
prompt = PromptTemplate(input_variables=["q"], template=prompt_template)

# 创建 PromptTemplate
prompt_wenti = PromptTemplate(input_variables=["wenti"], template=prompt_template_wenti)
prompt_jianli = PromptTemplate(input_variables=["jianli"], template=prompt_template_jianli)

# 使用 LLMChain 来组合 PromptTemplate 和 ChatOpenAI
#llm_chain = LLMChain(prompt=prompt, llm=agent)

# 创建模型链 已由管道符 代替 代码命令  LLMChain(llm=llm, prompt=prompt)
llm_chain = prompt | agent
llm_chain_wenti = prompt_wenti | agent
llm_chain_jianli = prompt_jianli | agent


# 停用词列表（这里可以加入你自己的停用词库），
stop_words = {'你', '给', '我', '一下', '是', '的', '在', '和', '。',',','？','说','知道','了解','讲','介绍','什么'}

def filter_stop_words(keywords):
    """去除停用词"""
    return [word for word in keywords if word not in stop_words]


def get_bot_answer(question):
    """获取聊天机器人回答"""
    q = question
    response = llm_chain.invoke(q)
    return response.content


def get_bot_answer_wenti(wenti):
    """获取聊天机器人回答,截图"""
    #print(wenti)
    response = llm_chain_wenti.invoke(wenti)
    return response.content


def get_bot_answer_jianli(jianli):
    """获取聊天机器人回答，制造简历"""
    response = llm_chain_jianli.invoke(jianli)
    return response.content


def get_kg_answer(query, db_name="knowledge/knowledge.db", top_n=3):
    """获取知识库回答"""
    # 连接数据库
    # 使用 jieba 进行中文分词
    keywords = list(jieba.cut(query))
    print(f"提取的关键词：{keywords}")

    # 去除停用词
    filtered_keywords = filter_stop_words(keywords)
    print(f"过滤后的关键词：{filtered_keywords}")

    # 连接数据库
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # 使用 LIKE 语句查找包含查询关键词的记录
    # 这里使用 '%' 来进行模糊匹配，匹配每个关键词
    results = []
    for keyword in filtered_keywords:
        cursor.execute("SELECT question, answer FROM knowledge WHERE question LIKE ?", ('%' + keyword + '%',))
        results += cursor.fetchall()

    # 去重，返回最相关的 top_n 条记录
    results = list(set(results))[:top_n]
    # 关闭数据库连接
    conn.close()
    return results
    # 如果有结果，返回最相关的记录
    # if results:
    #     print(f"找到 {len(results)} 条相关记录：")
    #     for idx, (question, answer) in enumerate(results, 1):
    #         print(f"{idx}. 问题: {question}\n   答案: {answer}\n")
    # else:
    #     print("没有找到相关记录。")


def capture_and_extract_text():
    """截取全屏并提取文本"""
    # 截取全屏
    screenshot = ImageGrab.grab()
    screenshot.save("assets/screenshot.png")

    # 使用Tesseract OCR提取文本
    text = pytesseract.image_to_string(screenshot, lang="chi_sim+eng")

    # 打印提取的文本（可选）
    #print(f"提取的文本: {text}")

    return text


# 生成 prompt.txt 文件
def generate_prompt(file_path):
    """根据文件路径提取信息并生成 prompt.txt"""

    # 读取文件内容（假设你已经提取文本并传递给此函数）
    """从 PDF 文件提取文本内容"""
    doc = fitz.open(file_path)
    jianli = ""
    for page in doc:
        jianli += page.get_text("text")  # 获取每一页的文本
    #print(jianli)
    #print('222')
    # 使用大模型提取简历信息
    extracted_info = get_bot_answer_jianli(
        jianli) + "\n上面是你的所有信息。简短有重点回答问题。你是目前正在寻找实习机会，现在你希望将你的技能应用于实际工作中。在这次面试中，你的工作是清晰地回答我的问题。你的回答应该简洁明了，抓住重点。无需过于正式，像正常与面试官交谈一样即可。你应该专注于清晰地解释你的思考过程，使用实际的例子（如果适用）。除非必要，否则避免使用过多的术语，力求回答简洁且能够体现你的技术能力。我会问你一些技术问题。你的任务是以展现你适合这个角色的方式回答问题。无论面试官问你什么，务必使用中文回答。问题: {q} 回答: "
    #print('333')
    # 生成 prompt.txt 文件
    with open("prompt/prompt.txt", "w", encoding="utf-8") as f:
        f.write(extracted_info)
    print("prompt.txt 已生成")
