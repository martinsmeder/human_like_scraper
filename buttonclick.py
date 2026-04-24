from camoufox.sync_api import Camoufox

with Camoufox(humanize=True) as browser:
    page = browser.new_page()
    page.goto("https://camoufox.com/tests/buttonclick")
    for _ in range(5):
        button = page.locator(".button") # create button locator
        button.wait_for() # wait until a .button element exists and is visible
        box = button.bounding_box() # get the button's position and size

        x = box["x"] + box["width"] / 2
        y = box["y"] + box["height"] / 2

        page.mouse.move(x, y)
        page.mouse.click(x, y)
