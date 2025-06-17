from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager


def make_chrome_browser(*options):
    chrome_options = webdriver.ChromeOptions()
    # Remove headless mode to run browser normally
    # chrome_options.add_argument('--headless')
    # Added options to prevent TensorFlow Lite XNNPACK delegate issue in headless Chrome
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-software-rasterizer')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    if options:
        for option in options:
            chrome_options.add_argument(option)
    chrome_service = ChromeService(ChromeDriverManager().install())
    browser = webdriver.Chrome(service=chrome_service, options=chrome_options)
    return browser


def make_firefox_browser(*options):
    firefox_options = webdriver.FirefoxOptions()
    # Remove headless mode to run browser normally
    # firefox_options.add_argument('--headless')
    # Added options to disable GPU and prevent related errors
    firefox_options.add_argument('--disable-gpu')
    firefox_options.add_argument('--no-sandbox')
    firefox_options.add_argument('--disable-dev-shm-usage')
    if options:
        for option in options:
            firefox_options.add_argument(option)
    firefox_service = FirefoxService(GeckoDriverManager().install())
    browser = webdriver.Firefox(service=firefox_service, options=firefox_options)
    return browser


def make_edge_browser(*options):
    edge_options = webdriver.EdgeOptions()
    # Remove headless mode to run browser normally
    # edge_options.add_argument('--headless')
    # Added options to disable GPU and prevent related errors
    edge_options.add_argument('--disable-gpu')
    edge_options.add_argument('--no-sandbox')
    edge_options.add_argument('--disable-dev-shm-usage')
    if options:
        for option in options:
            edge_options.add_argument(option)
    edge_service = EdgeService(EdgeChromiumDriverManager().install())
    browser = webdriver.Edge(service=edge_service, options=edge_options)
    return browser


if __name__ == '__main__':
    browser = make_chrome_browser('--headless')
    browser.get('https://google.com')
    sleep(5)
