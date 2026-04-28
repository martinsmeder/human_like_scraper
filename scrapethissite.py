import json
import os
import random
import time

from camoufox.sync_api import Camoufox


def pause(min_s, max_s=None):
    if max_s is None:
        max_s = min_s
    time.sleep(random.uniform(min_s, max_s))


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
        pause(0.12, 0.28)


def load_oscar_year(page, year):
    click(page, page.locator(f'a.year-link[id="{year}"]'))
    page.wait_for_function(
        """year => {
            const active_link = document.getElementById(year);
            const loading = document.querySelector("#loading");
            const rows = document.querySelectorAll("#table-body .film");
            return active_link &&
                active_link.classList.contains("active") &&
                loading &&
                getComputedStyle(loading).display === "none" &&
                rows.length > 0;
        }""",
        arg=year,
    )


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
    pause(0.7, 1.3)
    page.goto("https://www.scrapethissite.com/pages/")

    click_link(page, "Hockey Teams: Forms, Searching and Pagination")
    page.wait_for_url("**/pages/forms/")
    page.wait_for_selector(".team")
    scroll_down(page)
    pause(0.25, 0.6)
    click(page, page.locator("#per_page"))
    pause(0.2, 0.5)
    page.keyboard.press("End")
    pause(0.15, 0.4)
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
    pause(0.7, 1.3)
    page.goto("https://www.scrapethissite.com/pages/")
    pause(0.7, 1.3)

    click_link(page, "Oscar Winning Films: AJAX and Javascript")
    page.wait_for_url("**/pages/ajax-javascript/")
    page.wait_for_selector(".year-link")

    years = page.locator(".year-link").evaluate_all("els => els.map(e => e.id)")
    films = []
    for year in years:
        pause(0.25, 0.6)
        load_oscar_year(page, year)
        pause(0.2, 0.5)
        films += page.locator("#table-body .film").evaluate_all("""(els, year) => els.map(e => ({
            year: Number(year),
            title: e.querySelector(".film-title").innerText.trim(),
            nominations: Number(e.querySelector(".film-nominations").innerText),
            awards: Number(e.querySelector(".film-awards").innerText),
            best_picture: Boolean(e.querySelector(".film-best-picture .glyphicon-flag"))
        }))""", year)

    json.dump(films, open("output/oscar_winning_films.json", "w"), indent=2)
