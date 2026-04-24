from camoufox.sync_api import Camoufox

with Camoufox(humanize=True) as browser:
    page = browser.new_page()
    page.goto("https://www.scrapethissite.com/pages/")

    link = page.get_by_role("link", name="Countries of the World: A Simple Example")
    link.wait_for(state="visible")
    box = link.bounding_box()

    x = box["x"] + box["width"] / 2
    y = box["y"] + box["height"] / 2

    page.mouse.move(x, y)
    page.mouse.click(x, y)
