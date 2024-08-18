import re
import nest_asyncio; nest_asyncio.apply()
from playwright.sync_api import Playwright, sync_playwright
import pandas as pd
import os

da_remote = os.getenv("da_remote")
da_local = os.getenv("da_local")
de_remote = os.getenv("de_remote")
de_local = os.getenv("de_local")
keyword_local = os.getenv("keyword_local")
keyword_remote = os.getenv("keyword_remote")

job_sites = da_remote, da_local, de_remote, de_local, keyword_local, keyword_remote

def scrape():
    # Create an empty DataFrame
    df = pd.DataFrame(columns=['job_title', 'company', 'tech', 'url'])

    def run(playwright, site: str):
        browser = playwright.chromium.launch(headless=True, slow_mo=1000)
        context = browser.new_context()
        page = context.new_page()
        
        # Go to the job site
        page.goto(site)        
        # Wait for the elements to load
        page.wait_for_selector("div.relative")

        jobs = []

        # Find all job elements
        job_elements = page.query_selector_all("div.my-masonry-grid div.relative")
        
        for job_element in job_elements:
            # Hover over the job element
            job_element.hover()

            # Wait for any dynamic content to load
            page.wait_for_timeout(100)  # Adjust time as needed

            # Extract job details
            job_title = job_element.query_selector('span.line-clamp-2').inner_text()
            company = job_element.query_selector('span.line-clamp-1').inner_text()
            tech = job_element.query_selector('span.line-clamp-2.font-light').inner_text() if job_element.query_selector('span.line-clamp-2.font-light') else None,
            url = job_element.query_selector('a.z-10.text-black').get_attribute('href')

            jobs.append({
                'job_title': job_title,
                'company': company,
                'tech' : tech,
                'url': url,
            })
            
            
        browser.close()
        jobs_df = pd.DataFrame(jobs)
        return jobs_df
        
        
        # Close browser
        

    with sync_playwright() as playwright:
        for site in job_sites:
            jobs_df = run(playwright, site)
            df = pd.concat([df, jobs_df], ignore_index = True)

            # Convert jobs list to DataFrame
        
    df = df.drop_duplicates(ignore_index=True)
    
    return df


df = scrape()
df.to_csv("test.csv", index = False)


    
        
        


