import requests
import json
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler



async def cat_story():
    yandex_cloud_catalog = "b1ght86htrumpui6harn"
    yandex_api_key = ""
    temperature = 0.6
    prompt = "за что у тебя отвечает параметр temperature? Напиши математическую формулу"
    yandex_gpt_model = "yandexgpt-lite"
    body = {
        "modelUri": f"gpt://{yandex_cloud_catalog}/{yandex_gpt_model}",
        "completionOptions": {
            "stream": False,
            "temperature": temperature,
            "maxTokens": "2000",
        },
        "messages": [{"role": "user", "text": prompt}],
    }

    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {yandex_api_key}",
    }

    response = requests.post(url, headers=headers, json=body)
    response_json = json.loads(response.text)
    answer = response_json["result"]["alternatives"][0]["message"]["text"]
    print(answer)


