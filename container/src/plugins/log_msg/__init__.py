from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata
from nonebot import on_message
from .config import Config
import sqlite3
import time 
from nonebot.adapters import Event
from nonebot.rule import is_type
from nonebot.adapters.onebot.v11 import PrivateMessageEvent, GroupMessageEvent

__plugin_meta__ = PluginMetadata(
    name="log_msg",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

def insert_message_to_database(timeStamp,session_id, user_id, message):
    conn = sqlite3.connect('./chatDB.db')
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO messages (session_id,user_id, timeStamp, message) VALUES (?, ?, ?, ?)", (session_id, user_id,timeStamp, message))
    conn.commit()
    conn.close()
# 初始化插件，创建数据库
conn = sqlite3.connect('./chatDB.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS messages (
    session_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    timeStamp FLOAT NOT NULL,
    message TEXT NOT NULL
)''')
conn.commit()
conn.close()


rule = is_type(PrivateMessageEvent, GroupMessageEvent)
save_message = on_message(rule=rule,priority=5)

@save_message.handle()
async def handle_message(event: Event):
    message = event.get_plaintext().strip()
    user_id=event.get_user_id()
    session_id = event.get_session_id()
    timeStamp = time.time()
    insert_message_to_database(timeStamp,session_id, user_id, message)