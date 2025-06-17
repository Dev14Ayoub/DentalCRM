import unittest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.urls import reverse
from tests.functional_tests.base.base import BaseFunctionalTest

class UserRegisterTest(BaseFunctionalTest):

    def test_last_name_empty_error_message(self):
        self.browser.get(self.live_server_url + reverse('users:register'))
        
        # Find and clear last name field
        last_name_input = self.browser.find_element(By.NAME, 'last_name')
        self.browser.execute_script("arguments[0].value = '';", last_name_input)
        
        # Find and submit button using JavaScript
        submit_button = self.browser.find_element(
            By.CSS_SELECTOR, 'button[type="submit"]'
        )
        self.browser.execute_script("arguments[0].click();", submit_button)
        
        # Verify specific error message
        error_element = WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located((
                By.XPATH, 
                "//*[contains(text(), 'Last name cannot be empty')]"
            ))
        )
        self.assertTrue(error_element.is_displayed())