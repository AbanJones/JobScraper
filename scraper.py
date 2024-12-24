import re
import nest_asyncio; nest_asyncio.apply()
from playwright.sync_api import Playwright, sync_playwright
import pandas as pd


da = "https://hiring.cafe/?searchState=%7B%22higherOrderPrefs%22%3A%5B%22ANYWHERE_IN_STATE%22%2C%22ANYWHERE_IN_COUNTRY%22%2C%22ANYWHERE_IN_CONTINENT%22%2C%22ANYWHERE_IN_THE_WORLD%22%5D%2C%22geoLocRadius%22%3A35%2C%22preciseLocationPreference%22%3A%22NEAR_LOCALITY_AND_REMOTE_COUNTRY_FLEXIBLE%22%2C%22dateFetchedPastNDays%22%3A2%2C%22roleTypes%22%3A%5B%22Individual%20Contributor%22%5D%2C%22roleYoeRange%22%3A%5B0%2C2%5D%2C%22selectedPlaceDetail%22%3A%7B%22types%22%3A%5B%22locality%22%2C%22political%22%5D%2C%22formatted_address%22%3A%22Baltimore%2C%20Maryland%2C%20United%20States%22%2C%22geometry%22%3A%7B%22location%22%3A%7B%22lng%22%3A%22-76.61219000%22%2C%22lat%22%3A%2239.29038000%22%7D%7D%2C%22address_components%22%3A%5B%7B%22short_name%22%3A%22Baltimore%22%2C%22long_name%22%3A%22Baltimore%22%2C%22types%22%3A%5B%22locality%22%2C%22political%22%5D%7D%2C%7B%22types%22%3A%5B%22administrative_area_level_1%22%2C%22political%22%5D%2C%22long_name%22%3A%22Maryland%22%2C%22short_name%22%3A%22MD%22%7D%2C%7B%22short_name%22%3A%22US%22%2C%22types%22%3A%5B%22country%22%2C%22political%22%5D%2C%22long_name%22%3A%22United%20States%22%7D%5D%2C%22place_id%22%3A%22tSHYfhuuRdKcHIAynGsMQ%22%7D%2C%22searchQuery%22%3A%22data%20analyst%22%7D"

de = "https://hiring.cafe/?searchState=%7B%22searchQuery%22%3A%22data%20engineer%22%2C%22geoLocRadius%22%3A35%2C%22selectedPlaceDetail%22%3A%7B%22formatted_address%22%3A%22Baltimore%2C%20Maryland%2C%20United%20States%22%2C%22types%22%3A%5B%22locality%22%2C%22political%22%5D%2C%22geometry%22%3A%7B%22location%22%3A%7B%22lat%22%3A%2239.29038000%22%2C%22lng%22%3A%22-76.61219000%22%7D%7D%2C%22place_id%22%3A%22tSHYfhuuRdKcHIAynGsMQ%22%2C%22address_components%22%3A%5B%7B%22long_name%22%3A%22Baltimore%22%2C%22short_name%22%3A%22Baltimore%22%2C%22types%22%3A%5B%22locality%22%2C%22political%22%5D%7D%2C%7B%22long_name%22%3A%22Maryland%22%2C%22short_name%22%3A%22MD%22%2C%22types%22%3A%5B%22administrative_area_level_1%22%2C%22political%22%5D%7D%2C%7B%22long_name%22%3A%22United%20States%22%2C%22short_name%22%3A%22US%22%2C%22types%22%3A%5B%22country%22%2C%22political%22%5D%7D%5D%7D%2C%22dateFetchedPastNDays%22%3A2%2C%22roleYoeRange%22%3A%5B0%2C2%5D%2C%22roleTypes%22%3A%5B%22Individual%20Contributor%22%5D%2C%22preciseLocationPreference%22%3A%22NEAR_LOCALITY_AND_REMOTE_COUNTRY_FLEXIBLE%22%2C%22higherOrderPrefs%22%3A%5B%22ANYWHERE_IN_STATE%22%2C%22ANYWHERE_IN_COUNTRY%22%2C%22ANYWHERE_IN_CONTINENT%22%2C%22ANYWHERE_IN_THE_WORLD%22%5D%7D"

sql_python = "https://hiring.cafe/?searchState=%7B%22geoLocRadius%22%3A35%2C%22selectedPlaceDetail%22%3A%7B%22place_id%22%3A%22tSHYfhuuRdKcHIAynGsMQ%22%2C%22geometry%22%3A%7B%22location%22%3A%7B%22lat%22%3A%2239.29038000%22%2C%22lng%22%3A%22-76.61219000%22%7D%7D%2C%22address_components%22%3A%5B%7B%22short_name%22%3A%22Baltimore%22%2C%22long_name%22%3A%22Baltimore%22%2C%22types%22%3A%5B%22locality%22%2C%22political%22%5D%7D%2C%7B%22long_name%22%3A%22Maryland%22%2C%22short_name%22%3A%22MD%22%2C%22types%22%3A%5B%22administrative_area_level_1%22%2C%22political%22%5D%7D%2C%7B%22long_name%22%3A%22United%20States%22%2C%22short_name%22%3A%22US%22%2C%22types%22%3A%5B%22country%22%2C%22political%22%5D%7D%5D%2C%22formatted_address%22%3A%22Baltimore%2C%20Maryland%2C%20United%20States%22%2C%22types%22%3A%5B%22locality%22%2C%22political%22%5D%7D%2C%22higherOrderPrefs%22%3A%5B%22ANYWHERE_IN_STATE%22%2C%22ANYWHERE_IN_COUNTRY%22%2C%22ANYWHERE_IN_CONTINENT%22%2C%22ANYWHERE_IN_THE_WORLD%22%5D%2C%22roleYoeRange%22%3A%5B0%2C2%5D%2C%22roleTypes%22%3A%5B%22Individual%20Contributor%22%5D%2C%22preciseLocationPreference%22%3A%22NEAR_LOCALITY_AND_REMOTE_COUNTRY_FLEXIBLE%22%2C%22dateFetchedPastNDays%22%3A2%2C%22jobDescriptionQuery%22%3A%22%5C%22SQL%5C%22%20AND%20%5C%22Python%5C%22%5Cn%22%7D"

sql_excel = "https://hiring.cafe/?searchState=%7B%22selectedPlaceDetail%22%3A%7B%22place_id%22%3A%22tSHYfhuuRdKcHIAynGsMQ%22%2C%22formatted_address%22%3A%22Baltimore%2C%20Maryland%2C%20United%20States%22%2C%22address_components%22%3A%5B%7B%22long_name%22%3A%22Baltimore%22%2C%22short_name%22%3A%22Baltimore%22%2C%22types%22%3A%5B%22locality%22%2C%22political%22%5D%7D%2C%7B%22long_name%22%3A%22Maryland%22%2C%22short_name%22%3A%22MD%22%2C%22types%22%3A%5B%22administrative_area_level_1%22%2C%22political%22%5D%7D%2C%7B%22long_name%22%3A%22United%20States%22%2C%22types%22%3A%5B%22country%22%2C%22political%22%5D%2C%22short_name%22%3A%22US%22%7D%5D%2C%22geometry%22%3A%7B%22location%22%3A%7B%22lat%22%3A%2239.29038000%22%2C%22lng%22%3A%22-76.61219000%22%7D%7D%2C%22types%22%3A%5B%22locality%22%2C%22political%22%5D%7D%2C%22preciseLocationPreference%22%3A%22NEAR_LOCALITY_AND_REMOTE_COUNTRY_FLEXIBLE%22%2C%22jobDescriptionQuery%22%3A%22%5C%22SQL%5C%22%20AND%20%5C%22Excel%5C%22%5Cn%22%2C%22dateFetchedPastNDays%22%3A2%2C%22roleTypes%22%3A%5B%22Individual%20Contributor%22%5D%2C%22higherOrderPrefs%22%3A%5B%22ANYWHERE_IN_STATE%22%2C%22ANYWHERE_IN_COUNTRY%22%2C%22ANYWHERE_IN_CONTINENT%22%2C%22ANYWHERE_IN_THE_WORLD%22%5D%2C%22roleYoeRange%22%3A%5B0%2C2%5D%2C%22geoLocRadius%22%3A35%7D"

job_sites = da, de, sql_python, sql_excel

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
            tech_text = job_element.query_selector('span.line-clamp-2.font-light').inner_text() if job_element.query_selector('span.line-clamp-2.font-light') else None,
            tech_text = str(tech_text)
            tech_cleaned = re.sub(r"\(\s*'|'\s*\)", '', tech_text)
            url = job_element.query_selector('a.z-10.text-black').get_attribute('href')

            jobs.append({
                'job_title': job_title,
                'company': company,
                'tech' : tech_cleaned,
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




#test lines
""" df = scrape()
df.to_csv("test.csv", index = False) """


    
        
        


