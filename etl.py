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
        daily_jobs = scrape()
        load_dotenv()

        headers = {
            "Authorization": "Bearer " + os.getenv("NOTION_API_TOKEN"),
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
        }

        def get_pages(num_pages=None):
            """
            If num_pages is None, get all pages, otherwise just the defined number.
            """
            url = f"https://api.notion.com/v1/databases/{os.getenv('NOTION_DATABASE')}/query"

            get_all = num_pages is None
            page_size = 100 if get_all else num_pages

            payload = {"page_size": page_size}
            response = requests.post(url, json=payload, headers=headers)

            data = response.json()
            with open('db.json', 'w', encoding='utf8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            results = data["results"]
            while data.get("has_more") and get_all:
                payload = {"page_size": page_size, "start_cursor": data["next_cursor"]}
                response = requests.post(url, json=payload, headers=headers)
                data = response.json()
                results.extend(data["results"])

            return results
        
        def process_historical_jobs(results):
            jobs_data = []
            for result in results:
                try:
                    job_title = result["properties"]["Job Title"]["rich_text"][0]["text"]["content"]
                    company = result["properties"]["Company"]["title"][0]["text"]["content"]
                    tech_stack = result["properties"]["Tech Stack"]["rich_text"][0]["text"]["content"]
                    url = result["properties"]["Link"]["url"]
                    added_date = result["properties"]["Added Date"]["date"]["start"]

                    jobs_data.append({
                        "job_title": job_title,
                        "company": company,
                        "tech": tech_stack,
                        "url": url,
                        "added_date": added_date
                    })
                except KeyError as e:
                    logging.error(f"Key error when processing result: {e}")
            
            return pd.DataFrame(jobs_data)
        
        historical_jobs = 

        def create_page(data):
            url = "https://api.notion.com/v1/pages/"

            payload = {"parent": {"database_id": os.getenv("NOTION_DATABASE")}, "properties": data}

            res = requests.post(url, headers=headers, json=payload)
            
            if res.status_code != 200:
                logging.error(f"Failed to create page for {data['Job Title']['rich_text'][0]['text']['content']} with status code {res.status_code} and response: {res.text}")
            
            return res


        for index, row in daily_jobs.iterrows():
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