from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch(headless=False, slow_mo=1000)
    context = browser.new_context()
    page = context.new_page()
    
    page.goto('https://hiring.cafe/?searchState=%7B%22selectedPlaceDetail%22%3A%7B%22formatted_address%22%3A%22United%20States%22%2C%22place_id%22%3A%22user_country%22%2C%22geometry%22%3A%7B%22location%22%3A%7B%22lat%22%3A%2239.2891%22%2C%22lng%22%3A%22-76.5583%22%7D%7D%2C%22address_components%22%3A%5B%7B%22short_name%22%3A%22US%22%2C%22long_name%22%3A%22United%20States%22%2C%22types%22%3A%5B%22country%22%2C%22political%22%5D%7D%5D%2C%22types%22%3A%5B%22country%22%2C%22political%22%5D%7D%2C%22searchQuery%22%3A%5B%22Data%20Analyst%22%5D%2C%22hideJobTypes%22%3A%5B%22Saved%22%5D%2C%22workplaceTypes%22%3A%5B%22Remote%22%5D%2C%22dateFetchedPastNDays%22%3A%228%22%2C%22educationCredentials%22%3A%5B%22(Not%20Mentioned%20in%20Job%20Description)%22%2C%22License%20or%20Certificate%22%2C%22Trade%20School%20or%20Vocational%22%2C%22High%20School%22%2C%22Associate%22%2C%22Bachelors%22%5D%2C%22roleYoeRange%22%3A%5B0%2C2%5D%2C%22managementYoeRange%22%3A%5B0%2C0%5D%7D')  # Replace with your target URL
    
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
      
    for job in jobs:
        print(job)
    
    # Close browser
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
