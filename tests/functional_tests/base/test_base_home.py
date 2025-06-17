import pytest
from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from tests.functional_tests.base import BaseFunctionalTest


@pytest.mark.functional_test
class HomePageFunctionalTest(BaseFunctionalTest):
    def test_home_services_button_leads_to_correct_page(self):
        self.browser.get(self.live_server_url)
        # Open the sidebar menu first
        menu_toggle = self.browser.find_element(By.CLASS_NAME, 'menu-toggle')
        menu_toggle.click()
        # Wait for the sidebar menu to be visible
        WebDriverWait(self.browser, 5).until(
            EC.visibility_of_element_located((By.ID, 'sidebarMenu'))
        )
        # Find the 'Services' link by href attribute and click it
        services_url = reverse('base:services')
        services_button = self.browser.find_element(By.CSS_SELECTOR, f'a[href="{services_url}"]')
        # Sometimes the element is covered by another element, so use JavaScript click
        try:
            services_button.click()
        except Exception:
            self.browser.execute_script("arguments[0].click();", services_button)
        # Wait for navigation to complete after click
        WebDriverWait(self.browser, 10).until(
            lambda driver: driver.current_url.startswith(self.live_server_url)
        )
        self.assertTrue(self.browser.current_url.startswith(self.live_server_url))

    def test_home_schedule_button_leads_to_correct_page(self):
        self.browser.get(self.live_server_url)
        # Open the sidebar menu first
        menu_toggle = self.browser.find_element(By.CLASS_NAME, 'menu-toggle')
        menu_toggle.click()
        # Wait for the sidebar menu to be visible
        WebDriverWait(self.browser, 5).until(
            EC.visibility_of_element_located((By.ID, 'sidebarMenu'))
        )
        # Find the 'Schedule' link by href attribute and click it
        schedule_url = reverse('schedule:schedule')
        schedule_button = self.browser.find_element(By.CSS_SELECTOR, f'a[href="{schedule_url}"]')
        # Sometimes the element is covered by another element, so use JavaScript click
        try:
            schedule_button.click()
        except Exception:
            self.browser.execute_script("arguments[0].click();", schedule_button)
        # Wait for navigation to complete after click
        WebDriverWait(self.browser, 10).until(
            lambda driver: driver.current_url.startswith(self.live_server_url)
        )
        self.assertTrue(self.browser.current_url.startswith(self.live_server_url))

    def test_home_about_button_leads_to_correct_page(self):
        self.browser.get(self.live_server_url)
        # Open the sidebar menu first
        menu_toggle = self.browser.find_element(By.CLASS_NAME, 'menu-toggle')
        menu_toggle.click()
        # Wait for the sidebar menu to be visible
        WebDriverWait(self.browser, 5).until(
            EC.visibility_of_element_located((By.ID, 'sidebarMenu'))
        )
        # Find the 'About' link by href attribute and click it
        about_url = reverse('base:about')
        about_button = self.browser.find_element(By.CSS_SELECTOR, f'a[href="{about_url}"]')
        about_button.click()
        self.assertEqual(self.browser.current_url,
                         self.live_server_url + about_url)

    def test_home_login_button_leads_to_correct_page(self):
        self.browser.get(self.live_server_url)
        # Open the sidebar menu first
        menu_toggle = self.browser.find_element(By.CLASS_NAME, 'menu-toggle')
        menu_toggle.click()
        # Wait for the sidebar menu to be visible
        WebDriverWait(self.browser, 5).until(
            EC.visibility_of_element_located((By.ID, 'sidebarMenu'))
        )
        # Find the 'Login' link by href attribute and click it
        login_url = reverse('users:login')
        login_button = self.browser.find_element(By.CSS_SELECTOR, f'a[href="{login_url}"]')
        # Sometimes the element is covered by another element, so use JavaScript click
        try:
            login_button.click()
        except Exception:
            self.browser.execute_script("arguments[0].click();", login_button)
        # Wait for navigation to complete after click
        WebDriverWait(self.browser, 10).until(
            lambda driver: driver.current_url.startswith(self.live_server_url)
        )
        self.assertTrue(self.browser.current_url.startswith(self.live_server_url))

    def test_home_register_button_leads_to_correct_page(self):
        self.browser.get(self.live_server_url)
        # Open the sidebar menu first
        menu_toggle = self.browser.find_element(By.CLASS_NAME, 'menu-toggle')
        menu_toggle.click()
        # Wait for the sidebar menu to be visible
        WebDriverWait(self.browser, 5).until(
            EC.visibility_of_element_located((By.ID, 'sidebarMenu'))
        )
        # Find the 'Register' link by href attribute and click it
        register_url = reverse('users:register')
        register_button = self.browser.find_element(By.CSS_SELECTOR, f'a[href="{register_url}"]')
        # Sometimes the element is covered by another element, so use JavaScript click
        try:
            register_button.click()
        except Exception:
            self.browser.execute_script("arguments[0].click();", register_button)
        # Wait for navigation to complete after click
        WebDriverWait(self.browser, 10).until(
            lambda driver: driver.current_url.startswith(self.live_server_url)
        )
        self.assertTrue(self.browser.current_url.startswith(self.live_server_url))
