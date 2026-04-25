import json
import os
import time

from camoufox.sync_api import Camoufox


def click_link(page, name):
    link = page.get_by_role("link", name=name)
    link.wait_for(state="visible")
    box = link.bounding_box()
    x = box["x"] + box["width"] / 2
    y = box["y"] + box["height"] / 2
    page.mouse.move(x, y)
    page.mouse.click(x, y)

with Camoufox(humanize=True) as browser:
    page = browser.new_page()
    page.goto("https://www.scrapethissite.com/pages/")

    click_link(page, "Countries of the World: A Simple Example")

    page.wait_for_url("**/pages/simple/")
    page.wait_for_selector(".country")

    countries = page.locator(".country").evaluate_all("""els => els.filter(e => e.querySelector(".country-capital")).map(e => ({
        name: e.querySelector(".country-name").innerText.trim(),
        capital: e.querySelector(".country-capital").innerText.trim(),
        population: Number(e.querySelector(".country-population").innerText),
        area: Number(e.querySelector(".country-area").innerText)
    }))""")

    os.makedirs("output", exist_ok=True)
    json.dump(countries, open("output/countries.json", "w"), indent=2)
    time.sleep(1)
    page.goto("https://www.scrapethissite.com/pages/")

    click_link(page, "Hockey Teams: Forms, Searching and Pagination")
