# Page to practice on:
# https://camoufox.com/tests/buttonclick

from camoufox.sync_api import Camoufox

with Camoufox(humanize=True) as browser:
    page = browser.new_page()
    page.goto("https://camoufox.com/tests/buttonclick")
    for _ in range(5):
        button = page.locator(".button") # create button locator
        button.wait_for() # wait until a .button element exists and is visible
        box = button.bounding_box() # get the button's position and size

        page.mouse.move(
            box["x"] + box["width"] / 2,
            box["y"] + box["height"] / 2,
        )
        page.mouse.click(
            box["x"] + box["width"] / 2,
            box["y"] + box["height"] / 2,
        )
