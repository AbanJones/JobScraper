import re
import nest_asyncio; nest_asyncio.apply()
from playwright.sync_api import Playwright, sync_playwright

da_remote = "https://hiring.cafe/?searchState=%7B%22hideJobTypes%22%3A%5B%22Saved%22%5D%2C%22searchQuery%22%3A%5B%22Data%20Analyst%22%5D%2C%22selectedPlaceDetail%22%3A%7B%22types%22%3A%5B%22country%22%2C%22political%22%5D%2C%22address_components%22%3A%5B%7B%22short_name%22%3A%22US%22%2C%22types%22%3A%5B%22country%22%2C%22political%22%5D%2C%22long_name%22%3A%22United%20States%22%7D%5D%2C%22place_id%22%3A%22user_country%22%2C%22formatted_address%22%3A%22United%20States%22%2C%22geometry%22%3A%7B%22location%22%3A%7B%22lat%22%3A%2239.2891%22%2C%22lng%22%3A%22-76.5583%22%7D%7D%7D%2C%22managementYoeRange%22%3A%5B0%2C0%5D%2C%22roleYoeRange%22%3A%5B0%2C2%5D%2C%22workplaceTypes%22%3A%5B%22Remote%22%5D%2C%22dateFetchedPastNDays%22%3A%228%22%2C%22educationCredentials%22%3A%5B%22(Not%20Mentioned%20in%20Job%20Description)%22%2C%22License%20or%20Certificate%22%2C%22Trade%20School%20or%20Vocational%22%2C%22High%20School%22%2C%22Associate%22%2C%22Bachelors%22%5D%7D"

da_local = "https://hiring.cafe/?searchState=%7B%22searchQuery%22%3A%5B%22Data%20Analyst%22%5D%2C%22roleYoeRange%22%3A%5B0%2C2%5D%2C%22geoLocRadius%22%3A25%2C%22hideJobTypes%22%3A%5B%22Saved%22%5D%2C%22selectedPlaceDetail%22%3A%7B%22types%22%3A%5B%22locality%22%2C%22political%22%5D%2C%22formatted_address%22%3A%22Baltimore%2C%20MD%2C%20USA%22%2C%22geometry%22%3A%7B%22viewport%22%3A%7B%22northeast%22%3A%7B%22lat%22%3A39.37220594411627%2C%22lng%22%3A-76.52945281200961%7D%2C%22southwest%22%3A%7B%22lng%22%3A-76.71154072046406%2C%22lat%22%3A39.19720691882772%7D%7D%2C%22location%22%3A%7B%22lat%22%3A39.2903848%2C%22lng%22%3A-76.6121893%7D%7D%2C%22place_id%22%3A%22ChIJt4P01q4DyIkRWOcjQqiWSAQ%22%2C%22address_components%22%3A%5B%7B%22long_name%22%3A%22Baltimore%22%2C%22short_name%22%3A%22Baltimore%22%2C%22types%22%3A%5B%22locality%22%2C%22political%22%5D%7D%2C%7B%22types%22%3A%5B%22administrative_area_level_1%22%2C%22political%22%5D%2C%22short_name%22%3A%22MD%22%2C%22long_name%22%3A%22Maryland%22%7D%2C%7B%22short_name%22%3A%22US%22%2C%22types%22%3A%5B%22country%22%2C%22political%22%5D%2C%22long_name%22%3A%22United%20States%22%7D%5D%7D%2C%22dateFetchedPastNDays%22%3A%228%22%2C%22educationCredentials%22%3A%5B%22(Not%20Mentioned%20in%20Job%20Description)%22%2C%22License%20or%20Certificate%22%2C%22Trade%20School%20or%20Vocational%22%2C%22High%20School%22%2C%22Associate%22%2C%22Bachelors%22%5D%2C%22managementYoeRange%22%3A%5B0%2C0%5D%7D"


de_remote = "https://hiring.cafe/?searchState=%7B%22hideJobTypes%22%3A%5B%22Saved%22%5D%2C%22geoLocRadius%22%3A50%2C%22workplaceTypes%22%3A%5B%22Remote%22%5D%2C%22selectedPlaceDetail%22%3A%7B%22address_components%22%3A%5B%7B%22long_name%22%3A%22United%20States%22%2C%22types%22%3A%5B%22country%22%2C%22political%22%5D%2C%22short_name%22%3A%22US%22%7D%5D%2C%22place_id%22%3A%22ChIJCzYy5IS16lQRQrfeQ5K5Oxw%22%2C%22formatted_address%22%3A%22United%20States%22%2C%22geometry%22%3A%7B%22location%22%3A%7B%22lat%22%3A37.09024%2C%22lng%22%3A-95.712891%7D%2C%22viewport%22%3A%7B%22southwest%22%3A%7B%22lng%22%3A-173.2992296%2C%22lat%22%3A15.7760139%7D%2C%22northeast%22%3A%7B%22lng%22%3A-66.3193754%2C%22lat%22%3A72.7087158%7D%7D%7D%2C%22types%22%3A%5B%22country%22%2C%22political%22%5D%7D%2C%22roleYoeRange%22%3A%5B0%2C2%5D%2C%22educationCredentials%22%3A%5B%22(Not%20Mentioned%20in%20Job%20Description)%22%2C%22License%20or%20Certificate%22%2C%22Trade%20School%20or%20Vocational%22%2C%22High%20School%22%2C%22Associate%22%2C%22Bachelors%22%5D%2C%22dateFetchedPastNDays%22%3A%228%22%2C%22managementYoeRange%22%3A%5B0%2C0%5D%2C%22searchQuery%22%3A%5B%22Data%20Engineer%22%5D%7D"

de_local = "https://hiring.cafe/?searchState=%7B%22searchQuery%22%3A%5B%22Data%20Engineer%22%5D%2C%22hideJobTypes%22%3A%5B%22Saved%22%5D%2C%22managementYoeRange%22%3A%5B0%2C0%5D%2C%22dateFetchedPastNDays%22%3A%228%22%2C%22selectedPlaceDetail%22%3A%7B%22types%22%3A%5B%22locality%22%2C%22political%22%5D%2C%22formatted_address%22%3A%22Baltimore%2C%20MD%2C%20USA%22%2C%22geometry%22%3A%7B%22viewport%22%3A%7B%22northeast%22%3A%7B%22lng%22%3A-76.52945281200961%2C%22lat%22%3A39.37220594411627%7D%2C%22southwest%22%3A%7B%22lat%22%3A39.19720691882772%2C%22lng%22%3A-76.71154072046406%7D%7D%2C%22location%22%3A%7B%22lng%22%3A-76.6121893%2C%22lat%22%3A39.2903848%7D%7D%2C%22place_id%22%3A%22ChIJt4P01q4DyIkRWOcjQqiWSAQ%22%2C%22address_components%22%3A%5B%7B%22types%22%3A%5B%22locality%22%2C%22political%22%5D%2C%22short_name%22%3A%22Baltimore%22%2C%22long_name%22%3A%22Baltimore%22%7D%2C%7B%22types%22%3A%5B%22administrative_area_level_1%22%2C%22political%22%5D%2C%22long_name%22%3A%22Maryland%22%2C%22short_name%22%3A%22MD%22%7D%2C%7B%22types%22%3A%5B%22country%22%2C%22political%22%5D%2C%22long_name%22%3A%22United%20States%22%2C%22short_name%22%3A%22US%22%7D%5D%7D%2C%22educationCredentials%22%3A%5B%22(Not%20Mentioned%20in%20Job%20Description)%22%2C%22License%20or%20Certificate%22%2C%22Trade%20School%20or%20Vocational%22%2C%22High%20School%22%2C%22Associate%22%2C%22Bachelors%22%5D%2C%22geoLocRadius%22%3A25%2C%22roleYoeRange%22%3A%5B0%2C2%5D%7D"

job_sites = da_local, da_remote, de_local, de_remote


#print(job_sites)



playwright = sync_playwright().start()
browser = playwright.chromium.launch(headless=False, slow_mo=1000)
context = browser.new_context()
page = context.new_page()

#for site in job_sites:
page.goto(da_local)
page.wait_for_load_state("domcontentloaded")
page.locator("div").filter(has_text=re.compile(r"^Apply Directly$")).nth(1).click()


