import os
import requests
import pandas as pd
from datetime import datetime, timezone
from dotenv import load_dotenv, dotenv_values
from scraper import scrape
import json

df = scrape()
load_dotenv()

headers = {
    "Authorization": "Bearer " + os.getenv("NOTION_API_TOKEN"),
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}


 

def update_page(page_id: str, data: dict):
    url = f"https://api.notion.com/v1/pages/{page_id}"

    payload = {"properties": data}

    res = requests.patch(url, json=payload, headers=headers)
    print(res.status_code)
    return res

""" stage = "Offer"
color = "green"
update_data = {"Stage": {"status": {"name": stage, "color": color}}}

 """


for index, row in df.iterrows():
    data = {
        "Job Title": {"title": [{"text": {"content": row['job_title']}}]},
        "Company": {"rich_text": [{"text": {"content": row['company']}}]},
        "Technologies": {"rich_text": [{"text": {"content": row['tech']}}]},
        "URL": {"url": row['url']},
        "Stage": {"status": {"name": "To apply", "color": "default"}},  # Example status
    }


    update_page(os.getenv("NOTION_PAGE_ID"), data)