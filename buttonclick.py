from pathlib import Path

from camoufox.sync_api import Camoufox

with Camoufox() as browser:
    page = browser.new_page()
    page.goto(Path("buttonclick.html").resolve().as_uri())
    page.locator("button").last.wait_for()
    page.locator("button").last.click()
