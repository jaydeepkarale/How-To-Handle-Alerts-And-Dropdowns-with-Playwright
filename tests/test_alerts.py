import json
import os
import re
import subprocess
import sys
import urllib

import pytest
from dotenv import load_dotenv
from playwright.sync_api import expect, sync_playwright
from conftest import set_test_status

load_dotenv()

# # replace cloud_grid_page with local_grid_page while running on local
def test_handling_simple_alert(page):
    try:
        page.goto("https://www.lambdatest.com/selenium-playground/javascript-alert-box-demo")
        
        alert_text = None
        
        def handle_dialog(dialog):
            nonlocal alert_text
            alert_text = dialog.message
            dialog.dismiss()
        
        page.once("dialog", handle_dialog)
        page.locator("p").filter(has_text="JavaScript AlertsClick Me").get_by_role("button").click()
        
        assert alert_text == "I am an alert box!", f"Expected 'I am an alert box!' but got '{alert_text}'"
        set_test_status(page, 'Passed', 'Simple alert handling passed')
        page.close()
    except Exception as e:
        set_test_status(page, 'Failed', 'Simple alert handling failed', str(e))

def test_handling_confirm_box_accept(page):
    try:
        page.goto("https://www.lambdatest.com/selenium-playground/javascript-alert-box-demo")
        page.once("dialog", lambda dialog: dialog.accept())
        page.locator("p").filter(has_text="Confirm box:Click Me").get_by_role("button").click()
        expect(page.get_by_text("You pressed OK!", exact=True)).to_be_visible()
        set_test_status(page, 'Passed', 'Confirm box accept passed')
        page.close()
    except Exception as e:
        set_test_status(page, 'Failed', 'Confirm box accept failed', str(e))

def test_handling_confirm_box_dismss(page):
    try:
        page.goto("https://www.lambdatest.com/selenium-playground/javascript-alert-box-demo")
        page.once("dialog", lambda dialog: dialog.dismiss())
        page.locator("p").filter(has_text="Confirm box:Click Me").get_by_role("button").click()
        expect(page.get_by_text("You pressed Cancel!",exact=True)).to_be_visible()
        set_test_status(page, 'Passed', 'Confirm box dismiss passed')
        page.close()
    except Exception as e:
        set_test_status(page, 'Failed', 'Confirm box dismiss failed', str(e))

def test_handling_prompt_box(page):
    try:
        page.goto("https://www.lambdatest.com/selenium-playground/javascript-alert-box-demo")
        page.once("dialog", lambda dialog: dialog.accept('Jaydeep'))
        page.locator("p").filter(has_text="Prompt box:Click Me").get_by_role("button").click()
        expect(page.get_by_text("You have entered 'Jaydeep' !",exact=True)).to_be_visible()
        set_test_status(page, 'Passed', 'Prompt box handling passed')
        page.close()
    except Exception as e:
        set_test_status(page, 'Failed', 'Prompt box handling failed', str(e))

    
