from nonebot import get_driver

from .config import Config
from nonebot import on_command, on_message
from nonebot.rule import fullmatch
from nonebot.adapters import Message
from nonebot.adapters import Event
from nonebot.rule import keyword

global_config = get_driver().config
config = Config.parse_obj(global_config)

#创建事件响应器
rulePMTJ = fullmatch(("铺面推荐", "pmtj"), ignorecase=False)
Maprecommand = on_message(rule=rulePMTJ , priority=5, block=True)

@Maprecommand.handle()
async def handle_function(event: Event):
    await Maprecommand.finish("病友群铺面推荐\nhttps://docs.qq.com/sheet/DZFRkc2ZjbnlsemZN?tab=BB08J2")
    
