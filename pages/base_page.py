import logging


class BasePage:
    def __init__(self, page):
        self.page = page
        self.logger = logging.getLogger(self.__class__.__name__)

    def visit(self, url: str):
        self.logger.info(f"Navigating directly to target URL: {url}")
        # 🌐 DOMCONTENTLOADED — returns as soon as HTML is parsed,
        # without blocking on third-party ads/trackers finishing.
        # Never use the default "load" strategy on ad-heavy sandbox sites.
        self.page.goto(url, wait_until="domcontentloaded")

    def click_element(self, locator, timeout: float = 10000):
        self.logger.info(f"Waiting for and clicking element locator: {locator}")
        # ⏳ 10000ms gives slow-rendering pages time to paint elements
        # before we attempt interaction — prevents premature click failures.
        locator.wait_for(state="visible", timeout=timeout)
        locator.click()

    def type_text(self, locator, text: str, timeout: float = 10000):
        self.logger.info(f"Inputting secure text string into locator: {locator}")
        # ⏳ 10000ms matches click_element — consistent timeout policy
        # across all interaction methods in the framework.
        locator.wait_for(state="visible", timeout=timeout)
        # 🧹 Clear any pre-filled value before typing to avoid
        # appending to existing text (common bug in re-used form fields).
        locator.fill("")
        locator.fill(text)

    def wait_for_url_contains(self, substring: str, timeout: float = 10000):
        self.logger.info(f"Polling browser location until URL contains substring: {substring}")
        # 🔍 Waits until the browser URL matches the pattern.
        # Use this after clicks that trigger navigation to confirm
        # the redirect actually happened before asserting page content.
        self.page.wait_for_url(f"**{substring}**", timeout=timeout)
