import os
import requests
import pandas as pd
import logging
import json
from datetime import datetime, timezone
from dotenv import load_dotenv, dotenv_values
from scraper import *

logging.basicConfig(filename = "scrape_error.log", level = logging.ERROR, format = "%(asctime)s - %(levelname)s - %(message)s")

def main():
    try:
        df = scrape()
        load_dotenv()

        headers = {
            "Authorization": "Bearer " + os.getenv("NOTION_API_TOKEN"),
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
        }


        

        def create_page(data):
            url = "https://api.notion.com/v1/pages/"

            payload = {"parent": {"database_id": os.getenv("NOTION_DATABASE")}, "properties": data}

            res = requests.post(url, headers=headers, json=payload)
            
            if res.status_code != 200:
                logging.error(f"Failed to create page for {data['Job Title']['rich_text'][0]['text']['content']} with status code {res.status_code} and response: {res.text}")
            
            return res


        for index, row in df.iterrows():
            current_time = datetime.now()
            formatted_time = current_time.strftime("%Y-%m-%d")
            data = {
                "Stage": {"status": {"name": "To apply", "color": "default"}},  # default status
                "Job Title": {"rich_text": [{"text": {"content": row['job_title']}}]},
                "Company": {"title": [{"text": {"content": row['company']}}]},
                "Tech Stack": {"rich_text": [{"text": {"content": row['tech']}}]},
                "Link": {"url": row['url']},
                "Added Date": {"date": {"start": formatted_time}}
                
            }

            create_page(data)
            
    except Exception as e:
        logging.error("An error occured", exc_info = True)
        
        
if __name__ == "__main__":
    main()