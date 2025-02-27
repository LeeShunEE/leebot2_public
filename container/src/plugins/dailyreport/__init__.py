from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata
from nonebot import on_command, on_message
from .config import Config
import requests
from nonebot.adapters.onebot.v11 import MessageSegment
import os
import datetime
import time
__plugin_meta__ = PluginMetadata(
    name="dailyReport",
    description="",
    usage="",
    config=Config,
)
# 初始化插件，创建文件夹
config = get_plugin_config(Config)
if not os.path.exists(config.dailyReportDir):
        os.makedirs(config.dailyReportDir)
dailyReport = on_command("新闻", priority=5, block=True, aliases={"news", "早报", "zaobao", "zb", "Zb", "zaobao"})

@dailyReport.handle()
async def handle_function(event):
    current_date = datetime.datetime.today().strftime('%Y-%m-%d')
    file_path = config.dailyReportDir + f"/{current_date}.png"
    # 检查本日新闻是否已存在
    if os.path.exists(file_path):
        # 若已存在，赋值IMG
        with open(file_path, "rb") as f:
            data = f.read()
            img = MessageSegment.image(data)
    
    else:
    
    # 若不存在，则爬取新闻，然后存储，并赋值IMG
        url = "http://dwz.2xb.cn/zaob"
        response = requests.get(url)
        data = response.json()
        data_date = data.get("datatime")
        current_date = time.strftime("%Y-%m-%d", time.localtime())
        if data_date != current_date:
            await dailyReport.finish("今日新闻尚未发布")
        '''
        {
        "code": 200,
        "msg": "Success",
        "imageUrl": "https://g.gtimg.cn/music/photo_new/T053XD01003X5rBk2vN6jI.png",
        "datatime": "2024-11-05"
        }'''
        if response.status_code == 200:

            image_url = data.get("imageUrl")
            img_response = requests.get(image_url)
            with open(file_path, "wb") as f:
                f.write(img_response.content)
            img = MessageSegment.image(img_response.content)
            
        else:
            await dailyReport.finish("获取新闻失败")
    msg = f"新闻日期：{current_date}"
    await dailyReport.finish(msg + img)
    
# reset
reset = on_command("zbreset", priority=5, block=True)
@reset.handle()
async def handle_function(event):
    current_date = datetime.datetime.today().strftime('%Y-%m-%d')
    file_path = config.dailyReportDir + f"/{current_date}.png"
    if os.path.exists(file_path):
        os.remove(file_path)
        await reset.finish("已删除")
    else:
        await reset.finish("文件不存在")

