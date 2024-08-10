import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
   
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://hiring.cafe/")

    # ---------------------
 
    page.wait_for_timeout(300000)


with sync_playwright() as playwright:
    run(playwright)

    
    