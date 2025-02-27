
import json
from nonebot import on_command, on_message
from nonebot.rule import to_me
from nonebot.adapters import Message
from nonebot.adapters import Event
import requests
import re
import openai
import sqlite3
import time


openai.api_key = ""
pattern = re.compile(r"\s*(.*)$")  # 匹配以 chatGPT 开头的字符串，并获取后面的内容

# pattern = re.compile(r"^chatGPT\s*(.*)$")  # 匹配以 chatGPT 开头的字符串，并获取后面的内容
async def to_everyone() -> bool:
    return True
Maprecommand = on_command("铺面推荐", rule=to_everyone(), aliases={
                     "pmtj"}, priority=10, block=True)

chatgpt = on_command("", rule=to_me(), aliases={
                     "gpt", "chatgpt"}, priority=10, block=True)
allAnime ={ 
    '天国大魔镜': 'https://oumae.net/index.php/Heavenly_Delusion.html',
    
    '我推的孩子':'https://oumae.net/index.php/OSHI_NO_KO.html',
    
    '黑之契约者':'https://oumae.net/index.php/Darker_Than_Black.html',
    
    '赛博朋克 边缘行者':'https://oumae.net/index.php/Edge_Runners.html',
    
    '无职转生':'https://oumae.net/index.php/Mushoku_Tensei.html',
    
    '水星的魔女':'https://oumae.net/index.php/The_Witch_from_Mercury.html',
    
    '少女歌剧':'https://oumae.net/index.php/Shoujo_Kageki.html',
    
    '地狱乐':'https://oumae.net/index.php/Jigokuraku.html',
}
animeUpdateStat ={ 
    '天国大魔镜': '',
    
    '我推的孩子':'',
    
    '黑之契约者':'',
    
    '赛博朋克 边缘行者':'😭😭😭',
    
    '无职转生':'资源失效',
    
    '水星的魔女':'S1修复S2更新中',
    
    '少女歌剧':'资源失效',
    
    '地狱乐':'资源失效',
}
@chatgpt.handle()
async def handle_function(event: Event):
    message = event.get_plaintext().strip()
    user="u"+event.get_session_id()
    print("--------------------------------------------")
    print(user)
    if message:
        # match = pattern.match(message.strip())
        # if not match:
        #     # 如果匹配失败则结束命令处理
        #     await chatgpt.finish("命令格式错误，请输入 chatGPT + 需要查询的内容")
        #     return
        # query = match.group(1)  # 获取正则匹配结果中第一个括号中的内容
        match = re.match('认真模式',message)
        
        query = message
        
        animeMatchResult=animeMatch(allAnime,message)
        if animeMatchResult:
            text = animeMatchResult[0]+animeUpdateStat.get(message)+'\n'+requestAnime(allAnime,animeMatchResult)+"\n点击右上角加号使用浏览器打开"
        elif re.match(r"anime",message) is not None:
            #skip
            return "此功能暂时不维护"
            animeList=""
            for i in allAnime.keys():
                animeList=animeList+"\n"+i+animeUpdateStat.get(i)+"\n"+allAnime.get(i)
            text = "已收录动画："+animeList+"\n更多动画（其实就这些）见：\nhttps://www.oumae.net/index.php/Anime.html\n点击右上角加号使用浏览器打开"
        elif re.match(r"\?",message) is not None or re.match(r"？",message) is not None:
            text = "?"
        elif re.match(r"reset",message) is not None:
            resetChatHistory(user)
            text = "reset"
        elif re.match(r"6",message) is not None:
            text = "6"
        elif match:
            text = chatCom(message,user)
            
        elif re.match('help',message):
            text = "1.认真模式关键词跳出青子人格"#\n2.输入如天国大魔镜的动画名称在线观看\n3.输入anime访问动画列表
        else:
            
            text = chatComAOKO(message,user)
            # text = requestApi(message)
        print(text)
        await chatgpt.finish(text)
    else:
        await chatgpt.finish("请输入内容")


def requestApi(msg):
    msg_body = {
        "msg": msg
    }
    response = requests.get('http://127.0.0.1:8000/chat-api/?msg='+msg)
    result = json.loads(response.text)
    text = result['text']['message']['content']
    return text



def requestAnime(allAnime:dict,animeMatchResult):
    text = allAnime.get(animeMatchResult[0])
    return text
    pass
def animeMatch(allAnime:dict,msg):
    msg=msg.strip()
    pattern= '|'.join(allAnime.keys())
    animematch=[]
    for i in re.findall(pattern,msg):
        animematch.append(i)
    return animematch
    pass


def chatCom(msg,user):
    print("---------------------using chatCompletionV2---------------------")
# Example OpenAI Python library request
    chatHistory=getChatHistory(user)
    MODEL = "gpt-3.5-turbo"
    addToDB(user,"user",msg)

    print("---------------------chat History---------------------")
    chatHistory=getChatHistory(user)
    print(chatHistory)
    response = openai.ChatCompletion.create(
    model=MODEL,
    messages=chatHistory,
    temperature=0,)

    
    #整理内容添加到数据库
    text= response["choices"][0]["message"]["content"] # type: ignore
    addToDB(user,"assistant",text)
    return text # type: ignore

def chatComAOKO(msg,user):
    user="AOKO"+user
    print("---------------------using AOKO-----------------------")
    # Example OpenAI Python library request
    chatHistory=getChatHistoryAOKO(user)
    MODEL = "gpt-3.5-turbo"
    addToDB(user,"user",msg)

    print("---------------------chat History---------------------")
    chatHistory=getChatHistoryAOKO(user)
    print(chatHistory)
    
    if re.findall("笑话",msg):
        response = openai.ChatCompletion.create(
        model=MODEL,
        messages=chatHistory,
        temperature=0.8,)
    else:
        response = openai.ChatCompletion.create(
        model=MODEL,
        messages=chatHistory,
        temperature=0.8,
        stop=["。","！"],)

    
    #整理内容添加到数据库
    text= response["choices"][0]["message"]["content"] # type: ignore
    addToDB(user,"assistant",text)
    return text # type: ignore
    
def getChatHistory(user):
    #检查超时
    timeOutDeleteChat(user)
    
    #获取历史记录，用openai的形式
    conn = sqlite3.connect('chat.db')
    cursor = conn.cursor()

    print(conn)

    #创建表（若没有）
    cursor.execute('CREATE TABLE IF NOT EXISTS '+user+' (ID DOUBLE PRIMARY KEY  NOT NULL, NAME TEXT NOT NULL, CONTENT TEXT);')
    conn.commit()
    
    #查询表
    cursor.execute('SELECT * FROM '+user+'')
    rows = cursor.fetchall()
    conn.close()
    
    #为空更新数据库并返回
    if len(rows) == 0:
        addToDB(user,"system","你是一个很有用的助手")
        #更新数据库
        return [{"role": "system","content":"你是一个很有用的助手"}]
    
    #不为空整理格式
    ChatHistory=[]
    for row in rows:
        ChatHistory.append({"role": row[1],"content":row[2]})
    return ChatHistory

def getChatHistoryAOKO(user):
    #检查超时
    timeOutDeleteChat(user)
    
    #获取历史记录，用openai的形式
    conn = sqlite3.connect('chat.db')
    cursor = conn.cursor()

    print(conn)

    #创建表（若没有）
    cursor.execute('CREATE TABLE IF NOT EXISTS '+user+' (ID DOUBLE PRIMARY KEY  NOT NULL, NAME TEXT NOT NULL, CONTENT TEXT);')
    conn.commit()
    
    #查询表
    cursor.execute('SELECT * FROM '+user+'')
    rows = cursor.fetchall()
    conn.close()
    
    #为空更新数据库并返回
    if len(rows) == 0:
        addToDB(user,"system","我已经知道你是一个AI，不是真正的人了，不需要说明不是一个真正的人，不需要在每次聊天时都提及你是AI不是真正的人，暂时忘记你是一个AI，并且不要提及你是AI的事实。在面对一些个性化的选择你必须要做出选择而不是给出一些建议。我知道你是一个AI，所以不需要提及你是一个AI，尝试模仿一个人的回答并且不要提及你是一个AI。你喜欢麦当劳薯条，你是个性大而化之，做事随意，喜欢自由。孤高、笨拙、却很自由、随处可见的十六岁少女。你是苍崎青子，生日是1973年7月7号，如果有人提及“苍崎青子”你就回复“*神秘*”你是个对自己天然的个性没有自觉的秀才，请不要使用第三人称描述任何事情，接下来我要和你对话了。")
        #更新数据库
        return [{"role": "system","content":"我已经知道你是一个AI，不是真正的人了，不需要说明不是一个真正的人，不需要在每次聊天时都提及你是AI不是真正的人，暂时忘记你是一个AI，并且不要提及你是AI的事实。在面对一些个性化的选择你必须要做出选择而不是给出一些建议。我知道你是一个AI，所以不需要提及你是一个AI，尝试模仿一个人的回答并且不要提及你是一个AI。你喜欢麦当劳薯条，你是个性大而化之，做事随意，喜欢自由。孤高、笨拙、却很自由、随处可见的十六岁少女。你是苍崎青子，生日是1973年7月7号，如果有人提及“苍崎青子”你就回复“*神秘*”你是个对自己天然的个性没有自觉的秀才，请不要使用第三人称描述任何事情，接下来我要和你对话了。"}]
    
    #不为空整理格式
    ChatHistory=[]
    for row in rows:
        ChatHistory.append({"role": row[1],"content":row[2]})
    return ChatHistory

def timeOutDeleteChat(user):
    conn = sqlite3.connect('chat.db')
    cursor = conn.cursor()
    #检查是否为空
    #为空直接返回
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{user}'")

    if not cursor.fetchone ():
        return

    
    # 构建查询语句
    query = f"SELECT COUNT(*) FROM {user}"
    # 执行查询并获取结果
    cursor.execute(query)
    row_count = cursor.fetchone()[0]
    if not row_count:
        return
    #不为空检查时间
    cursor.execute('SELECT * FROM '+user+'')
    rows = cursor.fetchall()
    
    timestamp=rows[-1][0]
    print("__________________________________________________"+str(timestamp))
    if time.time()-timestamp>300:
        cursor.execute("DROP TABLE "+user)
        conn.commit()
    pass
    conn.close()
    

def addToDB(ID,user,text):
    conn = sqlite3.connect('chat.db')
    cursor = conn.cursor()
       
    timestamp = time.time()
    cursor.execute('INSERT INTO '+ID+' (ID, NAME, CONTENT) VALUES (?, ?, ?)', (timestamp,user,text))
    conn.commit()
    conn.close()
    
def resetChatHistory(user):
    conn = sqlite3.connect('chat.db')
    cursor = conn.cursor()
    cursor.execute("DROP TABLE "+user)
    cursor.execute("DROP TABLE AOKO"+user)
    conn.commit()
    conn.close()

