import pytest
import json
import os
import subprocess
import urllib
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright


load_dotenv()

capabilities = {
    'browserName': 'Chrome',
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
        'tunnel': False,
        'tunnelName': '',
        'geoLocation': '',
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
