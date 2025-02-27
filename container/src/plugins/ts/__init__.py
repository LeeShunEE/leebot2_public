from nonebot import get_driver
from nonebot import get_plugin_config
from .config import Config
from nonebot import on_command
from nonebot.adapters import Event


global_config = get_driver().config
config = get_plugin_config(Config)
#创建事件响应器
ts = on_command("ts" , priority=5, block=True)

# 创建消息
message = f"ts下载地址：\n\n{config.tsUrl}\n\nts服务器地址：{config.tsServerUrl}"

@ts.handle()
async def handle_function(event: Event):
    await ts.finish(message)
    
