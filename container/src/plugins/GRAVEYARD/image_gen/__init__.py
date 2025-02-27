from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata
from nonebot import on_command, on_message
from nonebot.rule import fullmatch,to_me
from nonebot.adapters import Message
from nonebot.adapters import Event
from nonebot.rule import keyword
from .config import Config
import json
import base64
import requests
from nonebot.adapters.onebot.v11 import MessageSegment

__plugin_meta__ = PluginMetadata(
    name="image_gen",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

#创建事件响应器
ruleIMG = fullmatch(("img",'Img',"setu","Setu"))
imgGen = on_command(rule=to_me(), aliases={"img", "Img","setu","Setu"}, priority=5, block=True,cmd=("img",'Img',"setu","Setu"))

def submit_post(url: str, data: dict):
    return requests.post(url, data=json.dumps(data))


def save_encoded_image(b64_image: str, output_path: str):
    with open(output_path, 'wb') as image_file:
        image_file.write(base64.b64decode(b64_image))



default_positive_prompt='''score_9, score_8_up, score_7_up, score_6_up, score_5_up, score_4_up, anime source'''

default_negative_prompt='''score_4, score_3, score_2, score_1  bad hands, missing fingers, (censor), monochrome, blurry  3d, source_cartoon  text, signature, watermark, username, artist name '''

adetail ={"ADetailer": {"args": [True, False, {"ad_cfg_scale": 7, "ad_checkpoint": "Use same checkpoint", "ad_clip_skip": 1, "ad_confidence": 0.3, "ad_controlnet_guidance_end": 1, "ad_controlnet_guidance_start": 0, "ad_controlnet_model": "None", "ad_controlnet_module": "None", "ad_controlnet_weight": 1, "ad_denoising_strength": 0.4, "ad_dilate_erode": 4, "ad_inpaint_height": 512, "ad_inpaint_only_masked": True, "ad_inpaint_only_masked_padding": 32, "ad_inpaint_width": 512, "ad_mask_blur": 4, "ad_mask_k_largest": 0, "ad_mask_max_ratio": 1, "ad_mask_merge_invert": "None", "ad_mask_min_ratio": 0, "ad_model": "face_yolov8n.pt", "ad_model_classes": "", "ad_negative_prompt": "", "ad_noise_multiplier": 1, "ad_prompt": "", "ad_restore_face": False, "ad_sampler": "DPM++ 2M", "ad_scheduler": "Use same scheduler", "ad_steps": 28, "ad_tab_enable": True, "ad_use_cfg_scale": False, "ad_use_checkpoint": False, "ad_use_clip_skip": False, "ad_use_inpaint_width_height": False, "ad_use_noise_multiplier": False, "ad_use_sampler": False, "ad_use_steps": False, "ad_use_vae": False, "ad_vae": "Use same VAE", "ad_x_offset": 0, "ad_y_offset": 0, "is_api": []}, {"ad_cfg_scale": 7, "ad_checkpoint": "Use same checkpoint", "ad_clip_skip": 1, "ad_confidence": 0.3, "ad_controlnet_guidance_end": 1, "ad_controlnet_guidance_start": 0, "ad_controlnet_model": "None", "ad_controlnet_module": "None", "ad_controlnet_weight": 1, "ad_denoising_strength": 0.4, "ad_dilate_erode": 4, "ad_inpaint_height": 512, "ad_inpaint_only_masked": True, "ad_inpaint_only_masked_padding": 32, "ad_inpaint_width": 512, "ad_mask_blur": 4, "ad_mask_k_largest": 0, "ad_mask_max_ratio": 1, "ad_mask_merge_invert": "None", "ad_mask_min_ratio": 0, "ad_model": "None", "ad_model_classes": "", "ad_negative_prompt": "", "ad_noise_multiplier": 1, "ad_prompt": "", "ad_restore_face": False, "ad_sampler": "DPM++ 2M", "ad_scheduler": "Use same scheduler", "ad_steps": 28, "ad_tab_enable": True, "ad_use_cfg_scale": False, "ad_use_checkpoint": False, "ad_use_clip_skip": False, "ad_use_inpaint_width_height": False, "ad_use_noise_multiplier": False, "ad_use_sampler": False, "ad_use_steps": False, "ad_use_vae": False, "ad_vae": "Use same VAE", "ad_x_offset": 0, "ad_y_offset": 0, "is_api": []}, {"ad_cfg_scale": 7, "ad_checkpoint": "Use same checkpoint", "ad_clip_skip": 1, "ad_confidence": 0.3, "ad_controlnet_guidance_end": 1, "ad_controlnet_guidance_start": 0, "ad_controlnet_model": "None", "ad_controlnet_module": "None", "ad_controlnet_weight": 1, "ad_denoising_strength": 0.4, "ad_dilate_erode": 4, "ad_inpaint_height": 512, "ad_inpaint_only_masked": True, "ad_inpaint_only_masked_padding": 32, "ad_inpaint_width": 512, "ad_mask_blur": 4, "ad_mask_k_largest": 0, "ad_mask_max_ratio": 1, "ad_mask_merge_invert": "None", "ad_mask_min_ratio": 0, "ad_model": "None", "ad_model_classes": "", "ad_negative_prompt": "", "ad_noise_multiplier": 1, "ad_prompt": "", "ad_restore_face": False, "ad_sampler": "DPM++ 2M", "ad_scheduler": "Use same scheduler", "ad_steps": 28, "ad_tab_enable": True, "ad_use_cfg_scale": False, "ad_use_checkpoint": False, "ad_use_clip_skip": False, "ad_use_inpaint_width_height": False, "ad_use_noise_multiplier": False, "ad_use_sampler": False, "ad_use_steps": False, "ad_use_vae": False, "ad_vae": "Use same VAE", "ad_x_offset": 0, "ad_y_offset": 0, "is_api": []}, {"ad_cfg_scale": 7, "ad_checkpoint": "Use same checkpoint", "ad_clip_skip": 1, "ad_confidence": 0.3, "ad_controlnet_guidance_end": 1, "ad_controlnet_guidance_start": 0, "ad_controlnet_model": "None", "ad_controlnet_module": "None", "ad_controlnet_weight": 1, "ad_denoising_strength": 0.4, "ad_dilate_erode": 4, "ad_inpaint_height": 512, "ad_inpaint_only_masked": True, "ad_inpaint_only_masked_padding": 32, "ad_inpaint_width": 512, "ad_mask_blur": 4, "ad_mask_k_largest": 0, "ad_mask_max_ratio": 1, "ad_mask_merge_invert": "None", "ad_mask_min_ratio": 0, "ad_model": "None", "ad_model_classes": "", "ad_negative_prompt": "", "ad_noise_multiplier": 1, "ad_prompt": "", "ad_restore_face": False, "ad_sampler": "DPM++ 2M", "ad_scheduler": "Use same scheduler", "ad_steps": 28, "ad_tab_enable": True, "ad_use_cfg_scale": False, "ad_use_checkpoint": False, "ad_use_clip_skip": False, "ad_use_inpaint_width_height": False, "ad_use_noise_multiplier": False, "ad_use_sampler": False, "ad_use_steps": False, "ad_use_vae": False, "ad_vae": "Use same VAE", "ad_x_offset": 0, "ad_y_offset": 0, "is_api": []}]}, "API payload": {"args": []}, "Comments": {"args": []}, "Extra options": {"args": []}, "Hypertile": {"args": []}, "Refiner": {"args": [False, "", 0.8]}, "Sampler": {"args": [20, "DPM++ 2M", "Automatic"]}, "Seed": {"args": [-1, False, -1, 0, 0, 0]}}
def img_request(prompt:str):
    txt2img_url = r'http://127.0.0.1:7861/sdapi/v1/txt2img'
    
    data = {
    "alwayson_scripts" :adetail,
    'prompt': default_positive_prompt+prompt,
    'negative_prompt': default_negative_prompt,
    'sampler_index': 'DPM++ 2M',
    'seed': -1,
    'steps': 48,
    'width': 1024,
    'height': 1024,
    'cfg_scale': 7}
    response = submit_post(txt2img_url, data)
    save_image_path = r'./tmp.png'
    # print(response.json())    
    return base64.b64decode(response.json()['images'][0])
    save_encoded_image(response.json()['images'][0], save_image_path)

@imgGen.handle()
async def handle_function(event: Event):
    message = event.get_plaintext().strip()
    for item in {"img", "Img","setu","Setu"}:
        message=message.strip(item)
    
    print(f"message:{message}")
    img = img_request(message)
    await imgGen.finish(MessageSegment.image(img))
    # for item in message:
    #     if "help" in item:
    #         await imgGen.finish("輸入提示詞")
    #     else:
    #         img = img_request(message)
    #         await imgGen.finish(MessageSegment.image(img))