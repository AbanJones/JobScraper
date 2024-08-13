import re
import nest_asyncio; nest_asyncio.apply()
from playwright.sync_api import Playwright, sync_playwright
import pandas as pd

def scrape():
    da_remote = "https://hiring.cafe/?searchState=%7B%22hideJobTypes%22%3A%5B%22Saved%22%5D%2C%22searchQuery%22%3A%5B%22Data%20Analyst%22%5D%2C%22selectedPlaceDetail%22%3A%7B%22types%22%3A%5B%22country%22%2C%22political%22%5D%2C%22address_components%22%3A%5B%7B%22short_name%22%3A%22US%22%2C%22types%22%3A%5B%22country%22%2C%22political%22%5D%2C%22long_name%22%3A%22United%20States%22%7D%5D%2C%22place_id%22%3A%22user_country%22%2C%22formatted_address%22%3A%22United%20States%22%2C%22geometry%22%3A%7B%22location%22%3A%7B%22lat%22%3A%2239.2891%22%2C%22lng%22%3A%22-76.5583%22%7D%7D%7D%2C%22managementYoeRange%22%3A%5B0%2C0%5D%2C%22roleYoeRange%22%3A%5B0%2C2%5D%2C%22workplaceTypes%22%3A%5B%22Remote%22%5D%2C%22dateFetchedPastNDays%22%3A%228%22%2C%22educationCredentials%22%3A%5B%22(Not%20Mentioned%20in%20Job%20Description)%22%2C%22License%20or%20Certificate%22%2C%22Trade%20School%20or%20Vocational%22%2C%22High%20School%22%2C%22Associate%22%2C%22Bachelors%22%5D%7D"
    da_local = "https://hiring.cafe/?searchState=%7B%22searchQuery%22%3A%5B%22Data%20Analyst%22%5D%2C%22roleYoeRange%22%3A%5B0%2C2%5D%2C%22geoLocRadius%22%3A25%2C%22hideJobTypes%22%3A%5B%22Saved%22%5D%2C%22selectedPlaceDetail%22%3A%7B%22types%22%3A%5B%22locality%22%2C%22political%22%5D%2C%22formatted_address%22%3A%22Baltimore%2C%20MD%2C%20USA%22%2C%22geometry%22%3A%7B%22viewport%22%3A%7B%22northeast%22%3A%7B%22lat%22%3A39.37220594411627%2C%22lng%22%3A-76.52945281200961%7D%2C%22southwest%22%3A%7B%22lng%22%3A-76.71154072046406%2C%22lat%22%3A39.19720691882772%7D%7D%2C%22location%22%3A%7B%22lat%22%3A39.2903848%2C%22lng%22%3A-76.6121893%7D%7D%2C%22place_id%22%3A%22ChIJt4P01q4DyIkRWOcjQqiWSAQ%22%2C%22address_components%22%3A%5B%7B%22long_name%22%3A%22Baltimore%22%2C%22short_name%22%3A%22Baltimore%22%2C%22types%22%3A%5B%22locality%22%2C%22political%22%5D%7D%2C%7B%22types%22%3A%5B%22administrative_area_level_1%22%2C%22political%22%5D%2C%22short_name%22%3A%22MD%22%2C%22long_name%22%3A%22Maryland%22%7D%2C%7B%22short_name%22%3A%22US%22%2C%22types%22%3A%5B%22country%22%2C%22political%22%5D%2C%22long_name%22%3A%22United%20States%22%7D%5D%7D%2C%22dateFetchedPastNDays%22%3A%228%22%2C%22educationCredentials%22%3A%5B%22(Not%20Mentioned%20in%20Job%20Description)%22%2C%22License%20or%20Certificate%22%2C%22Trade%20School%20or%20Vocational%22%2C%22High%20School%22%2C%22Associate%22%2C%22Bachelors%22%5D%2C%22managementYoeRange%22%3A%5B0%2C0%5D%7D"
    de_remote = "https://hiring.cafe/?searchState=%7B%22hideJobTypes%22%3A%5B%22Saved%22%5D%2C%22geoLocRadius%22%3A50%2C%22workplaceTypes%22%3A%5B%22Remote%22%5D%2C%22selectedPlaceDetail%22%3A%7B%22address_components%22%3A%5B%7B%22long_name%22%3A%22United%20States%22%2C%22types%22%3A%5B%22country%22%2C%22political%22%5D%2C%22short_name%22%3A%22US%22%7D%5D%2C%22place_id%22%3A%22ChIJCzYy5IS16lQRQrfeQ5K5Oxw%22%2C%22formatted_address%22%3A%22United%20States%22%2C%22geometry%22%3A%7B%22location%22%3A%7B%22lat%22%3A37.09024%2C%22lng%22%3A-95.712891%7D%2C%22viewport%22%3A%7B%22southwest%22%3A%7B%22lng%22%3A-173.2992296%2C%22lat%22%3A15.7760139%7D%2C%22northeast%22%3A%7B%22lng%22%3A-66.3193754%2C%22lat%22%3A72.7087158%7D%7D%7D%2C%22types%22%3A%5B%22country%22%2C%22political%22%5D%7D%2C%22roleYoeRange%22%3A%5B0%2C2%5D%2C%22educationCredentials%22%3A%5B%22(Not%20Mentioned%20in%20Job%20Description)%22%2C%22License%20or%20Certificate%22%2C%22Trade%20School%20or%20Vocational%22%2C%22High%20School%22%2C%22Associate%22%2C%22Bachelors%22%5D%2C%22dateFetchedPastNDays%22%3A%228%22%2C%22managementYoeRange%22%3A%5B0%2C0%5D%2C%22searchQuery%22%3A%5B%22Data%20Engineer%22%5D%7D"
    de_local = "https://hiring.cafe/?searchState=%7B%22searchQuery%22%3A%5B%22Data%20Engineer%22%5D%2C%22hideJobTypes%22%3A%5B%22Saved%22%5D%2C%22managementYoeRange%22%3A%5B0%2C0%5D%2C%22dateFetchedPastNDays%22%3A%228%22%2C%22selectedPlaceDetail%22%3A%7B%22types%22%3A%5B%22locality%22%2C%22political%22%5D%2C%22formatted_address%22%3A%22Baltimore%2C%20MD%2C%20USA%22%2C%22geometry%22%3A%7B%22viewport%22%3A%7B%22northeast%22%3A%7B%22lng%22%3A-76.52945281200961%2C%22lat%22%3A39.37220594411627%7D%2C%22southwest%22%3A%7B%22lat%22%3A39.19720691882772%2C%22lng%22%3A-76.71154072046406%7D%7D%2C%22location%22%3A%7B%22lng%22%3A-76.6121893%2C%22lat%22%3A39.2903848%7D%7D%2C%22place_id%22%3A%22ChIJt4P01q4DyIkRWOcjQqiWSAQ%22%2C%22address_components%22%3A%5B%7B%22types%22%3A%5B%22locality%22%2C%22political%22%5D%2C%22short_name%22%3A%22Baltimore%22%2C%22long_name%22%3A%22Baltimore%22%7D%2C%7B%22types%22%3A%5B%22administrative_area_level_1%22%2C%22political%22%5D%2C%22long_name%22%3A%22Maryland%22%2C%22short_name%22%3A%22MD%22%7D%2C%7B%22types%22%3A%5B%22country%22%2C%22political%22%5D%2C%22long_name%22%3A%22United%20States%22%2C%22short_name%22%3A%22US%22%7D%5D%7D%2C%22educationCredentials%22%3A%5B%22(Not%20Mentioned%20in%20Job%20Description)%22%2C%22License%20or%20Certificate%22%2C%22Trade%20School%20or%20Vocational%22%2C%22High%20School%22%2C%22Associate%22%2C%22Bachelors%22%5D%2C%22geoLocRadius%22%3A25%2C%22roleYoeRange%22%3A%5B0%2C2%5D%7D"

    job_sites = da_local, da_remote, de_local, de_remote


    # Create an empty DataFrame
    df = pd.DataFrame(columns=['job_title', 'company', 'tech', 'url'])



    for site in job_sites:
        def run(playwright):
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
                tech = job_element.query_selector('span.line-clamp-2.font-light').inner_text()
                url = job_element.query_selector('a.z-10.text-black').get_attribute('href')

                jobs.append({
                    'job_title': job_title,
                    'company': company,
                    'tech' : tech,
                    'url': url,
                })
                
                
            
            jobs_df = pd.DataFrame(jobs)
            global df
            df = pd.concat([df, jobs_df], ignore_index=True)
            
            # Close browser
            browser.close()

        with sync_playwright() as playwright:
            run(playwright) 

            # Convert jobs list to DataFrame
        
    df = df.drop_duplicates(ignore_index=True)
    df.to_csv('jobs.csv', index=False)        
        
        


