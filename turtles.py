import json
import os
import random
import re
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


def wait_for_turtle_list(frame):
    frame.wait_for_selector(".turtle-family-card")
    frame.wait_for_function(
        "() => document.querySelectorAll('.turtle-family-card').length > 0"
    )


def wait_for_turtle_detail(frame, family_name):
    frame.wait_for_selector(".turtle-family-detail")
    frame.wait_for_function(
        """family_name => {
            const heading = document.querySelector(".turtle-family-detail h3.family-name");
            return heading && heading.textContent.trim() === family_name;
        }""",
        arg=family_name,
    )


def get_turtle_links(frame):
    return frame.locator(".turtle-family-card").evaluate_all(
        """cards => cards.map(card => {
            const family_name = card.querySelector(".family-name").innerText.trim();
            const learn_more = card.querySelector("a");
            return {
                family_name,
                href: learn_more.getAttribute("href")
            };
        })"""
    )


def scrape_turtle_detail(frame):
    return frame.locator(".turtle-family-detail").evaluate(
        """detail => {
            const family_name = detail.querySelector("h3.family-name").innerText.trim();
            const common_name = detail.querySelector(".common-name").innerText.trim();
            const summary = detail.querySelector(".lead").innerText.trim();
            const match = summary.match(/were first discovered in (\\d+) by (.+)\\.$/);
            return {
                family_name,
                common_name,
                summary,
                discovered_year: match ? Number(match[1]) : null,
                discovered_by: match ? match[2] : null
            };
        }"""
    )


with Camoufox(humanize=True, window=(1280, 900)) as browser:
    page = browser.new_page()
    page.goto("https://www.scrapethissite.com/pages/")

    click_link(page, "Turtles All the Way Down: Frames & iFrames")
    page.wait_for_url("**/pages/frames/")
    page.wait_for_selector("#iframe")
    pause(0.4, 0.8)

    frame = page.frame(url=re.compile(r".*frame=i.*"))
    wait_for_turtle_list(frame)

    turtle_links = get_turtle_links(frame)
    turtles = []
    for turtle_link in turtle_links:
        family_name = turtle_link["family_name"]
        family_param = family_name.replace('"', '\\"')

        pause(0.2, 0.5)
        click(page, frame.locator(f'a[href*="family={family_param}"]'))
        wait_for_turtle_detail(frame, family_name)
        pause(0.2, 0.5)

        turtle = scrape_turtle_detail(frame)
        turtles.append(turtle)

        pause(0.2, 0.5)
        click(page, frame.get_by_role("link", name="Back to all Turtles"))
        wait_for_turtle_list(frame)
        pause(0.2, 0.5)

    os.makedirs("output", exist_ok=True)
    json.dump(turtles, open("output/turtles.json", "w"), indent=2)
