import requests
import os
from dotenv import load_dotenv

load_dotenv()
KV_REST_API_URL = os.environ.get("KV_REST_API_URL","")
KV_REST_API_TOKEN = os.environ.get("KV_REST_API_TOKEN","")

class RedisHelper:
    def __init__(self):
        self.KV_REST_API_URL = KV_REST_API_URL
        self.KV_REST_API_TOKEN = KV_REST_API_TOKEN
    def get(self,key):
        try:
            
            res = requests.get(f"{KV_REST_API_URL}/get/{key}",
                    headers={"Authorization":f"Bearer {KV_REST_API_TOKEN}"})
            if res.status_code == 200:
                return res.json()['result']
            return None
        except:
            return None

    def set(self,key,value):
        try:
            res = requests.post(f"{KV_REST_API_URL}",
                    headers={"Authorization":f"Bearer {KV_REST_API_TOKEN}"},
                    data=f'["SET", "{key}", "{value}"]')
            if res.status_code == 200:
                return res.json()
            return res.json()
        except:
            return None
    def delete(self,key):
        try:
            res = requests.post(f"{KV_REST_API_URL}",
                    headers={"Authorization":f"Bearer {KV_REST_API_TOKEN}"},
                    data=f'["DEL", "{key}"]')
            if res.status_code == 200:
                return res.json()
            return res.json()
        except:
            return None