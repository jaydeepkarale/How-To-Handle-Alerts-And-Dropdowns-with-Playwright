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
def test_handling_simple_alert(local_grid_page):
    local_grid_page.goto("https://www.lambdatest.com/selenium-playground/javascript-alert-box-demo")
    
    alert_text = None
    
    def handle_dialog(dialog):
        nonlocal alert_text
        alert_text = dialog.message
        dialog.dismiss()
    
    local_grid_page.once("dialog", handle_dialog)
    local_grid_page.locator("p").filter(has_text="JavaScript AlertsClick Me").get_by_role("button").click()
    
    # Now you can assert the alert text
    assert alert_text == "I am an alert box!", f"Expected 'I am an alert box!' but got '{alert_text}'"
        

def test_handling_confirm_box_accept(local_grid_page):
    local_grid_page.goto("https://www.lambdatest.com/selenium-playground/javascript-alert-box-demo")
    local_grid_page.once("dialog", lambda dialog: dialog.accept())
    local_grid_page.locator("p").filter(has_text="Confirm box:Click Me").get_by_role("button").click()
    expect(local_grid_page.get_by_text("You pressed OK!", exact=True)).to_be_visible()

def test_handling_confirm_box_dismss(local_grid_page):
    local_grid_page.goto("https://www.lambdatest.com/selenium-playground/javascript-alert-box-demo")
    local_grid_page.once("dialog", lambda dialog: dialog.dismiss())
    local_grid_page.locator("p").filter(has_text="Confirm box:Click Me").get_by_role("button").click()
    expect(local_grid_page.get_by_text("You pressed Cancel!",exact=True)).to_be_visible()


def test_handling_prompt_box(local_grid_page):
    
    local_grid_page.goto("https://www.lambdatest.com/selenium-playground/javascript-alert-box-demo")
    local_grid_page.once("dialog", lambda dialog: dialog.accept('Jaydeep'))
    local_grid_page.locator("p").filter(has_text="Prompt box:Click Me").get_by_role("button").click()
    expect(local_grid_page.get_by_text("You have entered 'Jaydeep' !",exact=True)).to_be_visible()

    
