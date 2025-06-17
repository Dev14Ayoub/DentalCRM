import pytest
from django.utils import translation
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException, WebDriverException
import time
from functools import wraps

from tests.functional_tests.base import BaseFunctionalTest


def retry_on_exception(exceptions, retries=5, delay=2):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exc = e
                    time.sleep(delay * (2 ** attempt))  # exponential backoff
            raise last_exc
        return wrapper
    return decorator


@pytest.mark.functional_test
class UserRegisterTest(BaseFunctionalTest):
    def get_form(self):
        return WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'main-form'))
        )

    def fill_form_dummy_data(self, form):
        fields = form.find_elements(By.TAG_NAME, 'input')
        for field in fields:
            if field.is_displayed():
                field.send_keys(' ' * 20)

    @retry_on_exception((StaleElementReferenceException, WebDriverException))
    def form_field_test_with_callback(self, callback):
        self.browser.get(self.live_server_url + '/users/register/')
        form = self.get_form()
        self.fill_form_dummy_data(form)
        email_field = WebDriverWait(form, 10).until(
            EC.presence_of_element_located((By.NAME, 'email'))
        )
        email_field.send_keys('dummy@email.com')
        callback(form)
        return form

    def fill_form_valid_data(self,
                             form,
                             first='First',
                             last='Last',
                             username='firstlast',
                             email='first@last.com',
                             password='P@ssw0rd',
                             phone_number=2499912345):
        self.get_by_placeholder(
            form, 'Enter your first name'
        ).send_keys(first)
        self.get_by_placeholder(
            form, 'Enter your last name'
        ).send_keys(last)
        self.get_by_placeholder(
            form, 'Enter a username'
        ).send_keys(username)
        self.get_by_placeholder(
            form, 'email@address.com'
        ).send_keys(email)
        self.get_by_placeholder(
            form, 'Enter your password'
        ).send_keys(password)
        self.get_by_placeholder(
            form, 'Enter your password again'
         ).send_keys(password)
        self.get_by_placeholder(
            form, '2499999999'
        ).send_keys(phone_number)

    def clear_field_and_submit(self, field, expected_error):
        """Helper method to clear a field and verify error message"""
        # Clear field using JavaScript
        self.browser.execute_script("arguments[0].value = '';", field)
        
        # Submit form using JavaScript
        submit_button = self.browser.find_element(
            By.CSS_SELECTOR, 'button[type="submit"]'
        )
        self.browser.execute_script("arguments[0].click();", submit_button)
        
        # Wait for specific error message
        error_element = WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located((
                By.XPATH, 
                f"//*[contains(text(), '{expected_error}')]"
            ))
        )
        self.assertTrue(error_element.is_displayed())

    @retry_on_exception((StaleElementReferenceException, ElementClickInterceptedException, WebDriverException))
    def test_first_name_empty_error_message(self):
        def callback(form):
            with translation.override('en'):
                first_name_field = self.get_by_placeholder(
                    form, 'Enter your first name'
                )
                self.clear_field_and_submit(
                    first_name_field, 
                    'First name cannot be empty'
                )
        self.form_field_test_with_callback(callback)

    @retry_on_exception((StaleElementReferenceException, ElementClickInterceptedException, WebDriverException))
    def test_last_name_empty_error_message(self):
        def callback(form):
            with translation.override('en'):
                last_name_field = self.get_by_placeholder(
                    form, 'Enter your last name'
                )
                self.clear_field_and_submit(
                    last_name_field, 
                    'Last name cannot be empty'
                )
        self.form_field_test_with_callback(callback)

    @retry_on_exception((StaleElementReferenceException, ElementClickInterceptedException, WebDriverException))
    def test_username_empty_error_message(self):
        def callback(form):
            with translation.override('en'):
                username_field = self.get_by_placeholder(
                    form, 'Enter a username'
                )
                self.clear_field_and_submit(
                    username_field, 
                    'Username is required'
                )
        self.form_field_test_with_callback(callback)

    @retry_on_exception((StaleElementReferenceException, ElementClickInterceptedException, WebDriverException))
    def test_passwords_do_not_match(self):
        def callback(form):
            with translation.override('en'):
                password1 = self.get_by_placeholder(
                    form, 'Enter your password'
                )
                password2 = self.get_by_placeholder(
                    form, 'Enter your password again'
                )
                password1.send_keys('P@ssw0rd')
                password2.send_keys('P@ssw0rd_different')
                
                # Submit using JavaScript
                submit_button = form.find_element(
                    By.CSS_SELECTOR, 'button[type="submit"]'
                )
                self.browser.execute_script("arguments[0].click();", submit_button)
                
                # Verify error
                error_element = WebDriverWait(self.browser, 10).until(
                    EC.visibility_of_element_located((
                        By.XPATH, 
                        "//*[contains(text(), 'Passwords must match')]"
                    ))
                )
                self.assertTrue(error_element.is_displayed())
        self.form_field_test_with_callback(callback)

    @retry_on_exception((StaleElementReferenceException, WebDriverException))
    def test_user_valid_data_register_success(self):
        with translation.override('en'):
            self.browser.get(self.live_server_url + '/users/register/')
            form = self.get_form()
            self.fill_form_valid_data(form)
            
            # Submit using JavaScript
            submit_button = form.find_element(
                By.CSS_SELECTOR, 'button[type="submit"]'
            )
            self.browser.execute_script("arguments[0].click();", submit_button)
            
            # Verify success
            WebDriverWait(self.browser, 10).until(
                EC.url_contains('/users/login/')
            )
            success_message = WebDriverWait(self.browser, 10).until(
                EC.visibility_of_element_located((
                    By.XPATH, 
                    "//*[contains(text(), 'User has been created, please log in')]"
                ))
            )
            self.assertTrue(success_message.is_displayed())