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
