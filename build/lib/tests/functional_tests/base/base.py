import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
import os

from utils.browser import make_chrome_browser, make_firefox_browser, make_edge_browser


class BaseFunctionalTest(StaticLiveServerTestCase):
    browser_type = os.getenv('BROWSER', 'chrome').lower()

    def setUp(self) -> None:
        if self.browser_type == 'firefox':
            self.browser = make_firefox_browser()
        elif self.browser_type == 'edge':
            self.browser = make_edge_browser()
        else:
            self.browser = make_chrome_browser()
        return super().setUp()

    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()

    def get_by_placeholder(self, web_element, placeholder):
        return web_element.find_element(
            By.XPATH, f'//input[@placeholder="{placeholder}"]'
        )

    def sleep(self, sec=2):  # pragma: no cover
        time.sleep(sec)
