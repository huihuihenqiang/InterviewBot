import base64
import os
import json
import requests
'''
语音识别
'''

def get_config():
    """从config.json中获取配置信息"""
    with open('config/config.json', 'r') as f:
        return json.load(f)


def get_access_token(api_key, secret_key):
    """获取access_token"""
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": api_key, "client_secret": secret_key}
    response = requests.post(url, params=params)
    return response.json().get("access_token")


def wav_to_base64(wav_file_path):
    """将WAV文件转换为Base64编码"""
    with open(wav_file_path, "rb") as f:
        wav_data = f.read()
    return base64.b64encode(wav_data).decode('utf-8')


def get_file_size(file_path):
    """获取文件大小"""
    return os.stat(file_path).st_size


def speech_to_text(wav_file_path):
    """将语音文件转换为文本"""
    config = get_config()
    api_key = config['API_KEY']
    secret_key = config['SECRET_KEY']
    cuid = config['CUID']

    url = "https://vop.baidu.com/server_api"
    access_token = get_access_token(api_key, secret_key)
    speech_base64 = wav_to_base64(wav_file_path)
    file_size = get_file_size(wav_file_path)

    payload = json.dumps({
        "format": "pcm",
        "rate": 16000,
        "channel": 1,
        "cuid": cuid,
        "speech": speech_base64,
        "len": file_size,
        "token": access_token,
    })
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, data=payload)
    return response.json()
