import json
import os
import re
import subprocess
import sys
import urllib

import pytest
from dotenv import load_dotenv
from playwright.sync_api import expect, sync_playwright


load_dotenv()

capabilities = {
    'browserName': 'Chrome',  # Browsers allowed: `Chrome`, `MicrosoftEdge`, `pw-chromium`, `pw-firefox` and `pw-webkit`
    'browserVersion': 'latest',
    'LT:Options': {
        'platform': 'Windows 11',
        'build': 'Playwright Locators Demo Build',
        'name': 'Playwright Locators Test For Windows 11 & Chrome',
        'user': os.getenv('LT_USERNAME'),
        'accessKey': os.getenv('LT_ACCESS_KEY'),
        'network': False,
        'video': True,
        'visual': False,
        'console': False,
        'tunnel': False,   # Add tunnel configuration if testing locally hosted webpage
        'tunnelName': '',  # Optional
        'geoLocation': '', # country code can be fetched from https://www.lambdatest.com/capabilities-generator/
    }
}


@pytest.fixture(name="local_grid_page")
def playwright_local_grid_page():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        page = browser.new_page()
        yield page

@pytest.fixture(name="cloud_grid_page")
def playwright_cloud_grid_page():    
    with sync_playwright() as playwright:
        playwrightVersion = str(subprocess.getoutput('playwright --version')).strip().split(" ")[1]
        capabilities['LT:Options']['playwrightClientVersion'] = playwrightVersion        
        lt_cdp_url = 'wss://cdp.lambdatest.com/playwright?capabilities=' + urllib.parse.quote(json.dumps(capabilities))    
        browser = playwright.chromium.connect(lt_cdp_url)
        page = browser.new_page()    
        yield page


# # replace cloud_grid_page with local_grid_page while running on local
def test_handling_simple_dropdown_by_value_or_label(local_grid_page):
    local_grid_page.goto("https://www.lambdatest.com/selenium-playground/select-dropdown-demo")
    local_grid_page.locator("#select-demo").select_option("Sunday")
    expect(local_grid_page.get_by_text("Day selected :- Sunday")).to_be_visible()


# # replace cloud_grid_page with local_grid_page while running on local
def test_handling_simple_dropdown_by_label(local_grid_page):
    local_grid_page.goto("https://www.lambdatest.com/selenium-playground/select-dropdown-demo")
    local_grid_page.locator("#select-demo").select_option(label='Monday')
    expect(local_grid_page.get_by_text("Day selected :- Monday")).to_be_visible()
    
    
# replace cloud_grid_page with local_grid_page while running on local
def test_handling_dropdown_with_search(local_grid_page):
    local_grid_page.goto("https://www.lambdatest.com/selenium-playground/jquery-dropdown-search-demo")
    local_grid_page.get_by_label("", exact=True).click(button="left")
    local_grid_page.pause()
    local_grid_page.get_by_role("textbox").nth(1).fill("India")
    expect(local_grid_page.get_by_role("treeitem", name="India")).to_be_visible()
