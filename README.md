# human_like_scraper

Small Camoufox-based scraping experiments focused on making browser automation
behave as human-like as possible.

## Main script

The main entrypoint is `scrapethissite.py`.

It scrapes several practice pages from
`https://www.scrapethissite.com/pages/` and writes the extracted data to
`output/` as JSON files.

The main goal of the script is mimic human browsing behavior.

- `Camoufox(humanize=True)` for humanized browser behavior
- real mouse movement and clicks based on element coordinates
- small randomized delays between interactions
- page-state waits based on DOM and URL changes instead of blind sleeping
- interacting with the site flow directly, including pagination, AJAX content,
  and iframe navigation

Current coverage in `scrapethissite.py`:

- Countries of the World
- Hockey Teams
- Oscar Winning Films
- Turtles All the Way Down

The advanced section is avoided for two reasons:

- Headers are spoofed by default with Camoufox
- Login practice requires you to buy their course

## Mouse test

`buttonclick.py` is a small standalone test used to verify simple human-like
mouse movement and clicking behavior against Camoufox's button click demo page.

## Run

Activate the virtual environment first:

```bash
source venv/bin/activate
```

Run the main scraper:

```bash
python3 scrapethissite.py
```
