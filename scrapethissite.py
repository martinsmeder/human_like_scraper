import json
import os
import time

from camoufox.sync_api import Camoufox


def click(page, target):
    target.wait_for(state="visible")
    target.scroll_into_view_if_needed()
    box = target.bounding_box()
    x = box["x"] + box["width"] / 2
    y = box["y"] + box["height"] / 2
    page.mouse.move(x, y)
    page.mouse.click(x, y)


def click_link(page, name):
    click(page, page.get_by_role("link", name=name))


def scroll_down(page):
    for _ in range(20):
        if page.evaluate("innerHeight + scrollY >= document.body.scrollHeight - 5"):
            break
        page.mouse.wheel(0, 1000)
        time.sleep(0.2)


with Camoufox(humanize=True, window=(1280, 900)) as browser:
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
    page.wait_for_url("**/pages/forms/")
    page.wait_for_selector(".team")
    scroll_down(page)
    time.sleep(0.5)
    click(page, page.locator("#per_page"))
    time.sleep(0.5)
    page.keyboard.press("End")
    time.sleep(0.5)
    page.keyboard.press("Enter")
    page.wait_for_url("**per_page=100**")
    page.wait_for_selector(".team")

    teams = []
    while True:
        teams += page.locator(".team").evaluate_all("""els => els.map(e => ({
            name: e.querySelector(".name").innerText.trim(),
            year: Number(e.querySelector(".year").innerText),
            wins: Number(e.querySelector(".wins").innerText),
            losses: Number(e.querySelector(".losses").innerText),
            ot_losses: Number(e.querySelector(".ot-losses").innerText) || null,
            win_pct: Number(e.querySelector(".pct").innerText),
            goals_for: Number(e.querySelector(".gf").innerText),
            goals_against: Number(e.querySelector(".ga").innerText),
            goal_diff: Number(e.querySelector(".diff").innerText)
        }))""")

        scroll_down(page)
        next_link = page.locator('a[aria-label="Next"]')
        if not next_link.count():
            break
        url = page.url
        click(page, next_link)
        page.wait_for_url(lambda next_url: next_url != url)
        page.wait_for_selector(".team")

    json.dump(teams, open("output/hockey_teams.json", "w"), indent=2)
    time.sleep(1)
    page.goto("https://www.scrapethissite.com/pages/")
    time.sleep(1)
