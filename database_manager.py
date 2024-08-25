import requests
import os
import json
from supabase import create_client, Client
from postgrest.exceptions import APIError
from dotenv import load_dotenv, dotenv_values
from datetime import datetime




load_dotenv()

supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

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

def insert_into_supabase(data):
    """
    Insert data into the Supabase table, skip if duplicate.
    """
    try:
        response = supabase.table('jobs').insert(data).execute()
        print("Row successfully inserted into Supabase.")
    except APIError as e:
        error_details = e.args[0]  # Extract the error details

        try:
            error_details = json.loads(error_details)  # Attempt to parse as JSON
        except (json.JSONDecodeError, TypeError):
            pass  # If it's not JSON, keep it as a string

        # Handle as a dictionary if possible
        if isinstance(error_details, dict) and error_details.get('code') == '23505':  # Duplicate key error
            print(f"Duplicate entry found for URL {data['Link']}, skipping.")
        else:
            print("Failed to insert row into Supabase:", error_details)

# Fetch pages from Notion
pages = get_pages()

# Iterate through each page and extract the necessary fields
for page in pages:
    page_id = page["id"]
    props = page["properties"]
    
    # Extract the properties based on the structure of your JSON
    job_title = props["Job Title"]["rich_text"][0]["text"]["content"]
    tech_stack = props["Tech Stack"]["rich_text"][0]["text"]["content"]
    stage = props["Stage"]["status"]["name"]
    url = props["Link"]["url"]
    company = props["Company"]["title"][0]["text"]["content"]


    current_timestamp = datetime.now().isoformat()

    # Prepare data to insert into Supabase
    data = {
        "job_title": job_title,
        "company": company,
        "tech_stack": tech_stack,
        "url": url,
        "added_date": current_timestamp
    }

    # Insert data into Supabase
    #insert_into_supabase(data)
