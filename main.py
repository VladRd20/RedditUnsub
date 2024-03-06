from playwright.sync_api import Playwright, sync_playwright
from time import sleep
from bs4 import BeautifulSoup
from sys import argv


url = "https://www.reddit.com/r/"
names = []
count = 0
try:
    username = str(argv[1])
    password = str(argv[2])
    print("Successfully read username and password from command line arguments.")
except IndexError:
    print("Usage: python main.py <username> <password>")
    exit(1)


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    print("Launched browser.")
    page.goto("https://www.reddit.com/subreddits")
    print("Opened reddit.com/subreddits")
    page.get_by_placeholder("username").fill(username)
    page.get_by_placeholder("password").fill(password)
    page.get_by_role("button", name="login").click()
    print("Logged in.")
    sleep(5)
    html = page.inner_html("html")
    soup = BeautifulSoup(html, "html.parser")

    for li in soup.find_all("li"):
        if li.text.startswith("leave"):
            names.append(li.text.replace("leave", "").replace("join", ""))
    count = len(names)
    print(f"Found {count} subreddits to leave.")

    for name in names:
        page.goto(url + name)
        page.get_by_role("button", name="Joined").click()
        count -= 1
        print(f"Left {name}. | {count} remaining.")

    # ---------------------
    print("Finished leaving subreddits.")
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
