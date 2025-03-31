import pytest
import json
import os
import subprocess
import urllib
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright, Page


load_dotenv()

run_on = os.getenv("RUN_ON") or 'local'

def set_test_status(page: Page, status: str, remark: str):
    """
    Function to set stats, title and description of test run on cloud grid
    :param page: instance of Playwright browser page
    :param status: status of test e.g Pass or Failed
    :param remark: additional remark about test status
    """
    page.evaluate(
        "_ => {}",
        "lambdatest_action: {\"action\": \"setTestStatus\", \"arguments\": {\"status\":\"" + status + "\", \"remark\": \"" + remark + "\"}}"
    )
    

capabilities = {
    'browserName': 'Chrome',
    'browserVersion': 'latest',
    'LT:Options': {
        'platform': 'Windows 11',
        'build': 'Playwright Dropdown Demo Build',
        'name': 'Playwright Dropdown Test For Windows 11 & Chrome',
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

@pytest.fixture(name="browser")
def playwright_browser():     
    if run_on == 'local':
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=False)
            yield browser
    
    if run_on == 'cloud':
        with sync_playwright() as playwright:
            playwrightVersion = str(subprocess.getoutput('playwright --version')).strip().split(" ")[1]
            capabilities['LT:Options']['playwrightClientVersion'] = playwrightVersion        
            lt_cdp_url = 'wss://cdp.lambdatest.com/playwright?capabilities=' + urllib.parse.quote(json.dumps(capabilities))
            browser = playwright.chromium.connect(lt_cdp_url)
            yield browser   


@pytest.fixture(name="page")
def page(browser):
    page = browser.new_context().new_page()        
    yield page
    browser.close()
