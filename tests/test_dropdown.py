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

def test_handling_simple_dropdown_by_value_or_label(page):
    try:
        page.goto("https://www.lambdatest.com/selenium-playground/select-dropdown-demo")
        page.locator("#select-demo").select_option("Sunday")
        expect(page.get_by_text("Day selected :- Sunday")).to_be_visible()
        set_test_status(page, 'Passed','Simple dropdown by value or label passed')
        page.close()
    except Exception as e:
        set_test_status(page, 'Failed','Simple dropdown by value or label failed', str(e))

def test_handling_simple_dropdown_by_label(page):
    try:
        page.goto("https://www.lambdatest.com/selenium-playground/select-dropdown-demo")
        page.locator("#select-demo").select_option(label='Monday')
        expect(page.get_by_text("Day selected :- Monday")).to_be_visible()
        set_test_status(page, 'Passed', 'Simple dropdown by label passed')
        page.close()
    except Exception as e:
        set_test_status(page, 'Failed', 'Simple dropdown by label failed', str(e))

def test_handling_dropdown_with_search(page):
    try:
        page.goto("https://www.lambdatest.com/selenium-playground/jquery-dropdown-search-demo")
        page.get_by_label("", exact=True).click(button="left")
        page.get_by_role("textbox").nth(1).fill("India")
        expect(page.get_by_role("treeitem", name="India")).to_be_visible()
        set_test_status(page, 'Passed', 'Dropdown with search passed')
        page.close()
    except Exception as e:
        set_test_status(page, 'Failed', 'Dropdown with search failed', str(e))
