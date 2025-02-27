

import openai
import sqlite3
import time

conn = sqlite3.connect('chat.db')
cursor = conn.cursor()
user="u2457013396"
print(conn)
#创建表
cursor.execute('CREATE TABLE IF NOT EXISTS '+user+' (ID DOUBLE PRIMARY KEY NOT NULL, NAME TEXT NOT NULL, CONTENT TEXT);')
conn.commit()
cursor.execute('SELECT * FROM '+user+'')
rows = cursor.fetchall()

#插入内容
timestamp = time.time()
cursor.execute('INSERT INTO '+user+' (ID, NAME, CONTENT) VALUES (?, ?, ?)', (timestamp,'John','你好'))
timestamp = time.time()+1
cursor.execute('INSERT INTO '+user+' (ID, NAME, CONTENT) VALUES (?, ?, ?)', (timestamp,'John','我好'))
conn.commit()

#查询表
cursor.execute('SELECT * FROM '+user+'')
rows = cursor.fetchall()

# 检索查询结果
result = cursor.fetchall()
# 打印查询结果
for row in result:
    print(row)

cursor.close()
conn.close()





def chatCom(msg,user):
    print("---------------------using chatCompletionV2---------------------")
# Example OpenAI Python library request
    chatHistory=getChatHistory(user)
    
    MODEL = "gpt-3.5-turbo"
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=chatHistory.append({"role": "user", "content": msg}),
        temperature=0,
    )
    #整理内容添加到数据库
    text= response["choices"][0]["message"]["content"] # type: ignore
    addToDB(user,text)
    return response["choices"][0]["message"]["content"] # type: ignore

def chatComAOKO(msg,user):
    
# Example OpenAI Python library request
    MODEL = "gpt-3.5-turbo"
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Knock knock."},
            {"role": "assistant", "content": "Who's there?"},
            {"role": "user", "content": "Orange."},
        ],
        temperature=0.5,
    )
    
def getChatHistory(user):
    #检查超时
    timeOutDeleteChat(user)
    
    #获取历史记录，用openai的形式
    conn = sqlite3.connect('chat.db')
    cursor = conn.cursor()
    user="u"+user
    print(conn)

    #创建表（若没有）
    cursor.execute('CREATE TABLE IF NOT EXISTS '+user+' (ID DOUBLE PRIMARY KEY  NOT NULL, NAME TEXT NOT NULL, CONTENT TEXT);')
    conn.commit()
    
    #查询表
    cursor.execute('SELECT * FROM '+user+'')
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    #为空直接返回
    if len(rows) == 0:
        return []
    #不为空整理格式
    ChatHistory=[{"role": "system","content":"你是一个很有用的助手"}]
    for row in rows:
        ChatHistory.append({"role": row[1],"content":row[2]})
    return ChatHistory
    
    #插入内容
    timestamp = time.time()
    cursor.execute('INSERT INTO '+user+' (ID, NAME, CONTENT) VALUES (?, ?, ?)', (timestamp,'user','你好'))
    timestamp = time.time()+1
    cursor.execute('INSERT INTO '+user+' (ID, NAME, CONTENT) VALUES (?, ?, ?)', (timestamp,'user','我好'))
    conn.commit()

    #查询表
    cursor.execute('SELECT * FROM '+user+'')
    rows = cursor.fetchall()

    # 检索查询结果
    result = cursor.fetchall()
    # 打印查询结果
    for row in result:
        print(row)

    cursor.close()
    conn.close()
    pass

def timeOutDeleteChat(user):
    conn = sqlite3.connect('chat.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM '+user+'')
    rows = cursor.fetchall()
    print(rows)
    if time.time()-rows[-1]["ID"]>300:
        cursor.execute("DROP TABLE "+user)
    pass

def addToDB(user,text):
    conn = sqlite3.connect('chat.db')
    cursor = conn.cursor()
    user="u"+user
    print(conn)
    timestamp = time.time()
    cursor.execute('INSERT INTO '+user+' (ID, NAME, CONTENT) VALUES (?, ?, ?)', (timestamp,'user','你好'))