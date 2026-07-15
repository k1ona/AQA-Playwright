# scripts/capture_notes_snapshot.py
# One-off utility to save a logged-in snapshot of the notes app for offline
# locator inspection. Not part of the test suite — run manually when needed.

import os

from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

load_dotenv()

EMAIL = os.getenv("NOTES_EMAIL")
PASSWORD = os.getenv("NOTES_PASSWORD")

if not EMAIL or not PASSWORD:
    raise SystemExit("NOTES_EMAIL or NOTES_PASSWORD not found — check your .env file.")

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()

    page.goto("https://practice.expandtesting.com/notes/app/login")
    page.fill("#email", EMAIL)
    page.fill("#password", PASSWORD)
    page.click("button[type='submit']")

    page.wait_for_load_state("networkidle")

    html = page.content()
    with open("reference_vault/expandtesting/notes_app.html", "w", encoding="utf-8") as f:
        f.write(html)

    browser.close()

print("Saved notes app snapshot.")
