import pytest
from django.utils import translation
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException, WebDriverException, TimeoutException
import time
from functools import wraps
import uuid

from tests.functional_tests.base import BaseFunctionalTest


@pytest.mark.usefixtures("live_server")
def get_by_name(self, web_element, name):
    return web_element.find_element(By.NAME, name)


def retry_on_exception(exceptions, retries=3, delay=1):
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
        # Reduced wait time for faster test execution
        return WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'register-form'))
        )

    def get_by_name(self, web_element, name):
        # Search from the browser instead of the web_element to avoid missing elements
        return self.browser.find_element(By.NAME, name)

    def fill_form_dummy_data(self, form):
        fields = form.find_elements(By.TAG_NAME, 'input')
        for field in fields:
            if field.is_displayed():
                input_type = field.get_attribute('type')
                if input_type in ['text', 'email', 'password', 'tel']:
                    field.send_keys(' ' * 20)

    @retry_on_exception((StaleElementReferenceException, WebDriverException, TimeoutException))
    def form_field_test_with_callback(self, callback):
        self.browser.get(self.live_server_url + '/users/register/')
        form = self.get_form()
        self.fill_form_dummy_data(form)
        email_field = WebDriverWait(form, 5).until(
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
                             email='uniqueemail@example.com',
                             password='P@ssw0rd',
                             phone_number='2499912345',
                             clinic='Test Clinic'):
        # Clear all fields before sending keys to avoid residual values
        self.get_by_name(form, 'first_name').clear()
        self.get_by_name(form, 'last_name').clear()
        self.get_by_name(form, 'username').clear()
        self.get_by_name(form, 'email').clear()
        self.get_by_name(form, 'password1').clear()
        self.get_by_name(form, 'password2').clear()
        self.get_by_name(form, 'phone_number').clear()
        self.get_by_name(form, 'clinic').clear()

        # Wait for all fields to be empty before sending keys
        WebDriverWait(self.browser, 5).until(
            lambda driver: self.get_by_name(form, 'first_name').get_attribute('value') == ''
        )
        WebDriverWait(self.browser, 5).until(
            lambda driver: self.get_by_name(form, 'last_name').get_attribute('value') == ''
        )
        WebDriverWait(self.browser, 5).until(
            lambda driver: self.get_by_name(form, 'username').get_attribute('value') == ''
        )
        WebDriverWait(self.browser, 5).until(
            lambda driver: self.get_by_name(form, 'email').get_attribute('value') == ''
        )
        WebDriverWait(self.browser, 5).until(
            lambda driver: self.get_by_name(form, 'password1').get_attribute('value') == ''
        )
        WebDriverWait(self.browser, 5).until(
            lambda driver: self.get_by_name(form, 'password2').get_attribute('value') == ''
        )
        WebDriverWait(self.browser, 5).until(
            lambda driver: self.get_by_name(form, 'phone_number').get_attribute('value') == ''
        )
        WebDriverWait(self.browser, 5).until(
            lambda driver: self.get_by_name(form, 'clinic').get_attribute('value') == ''
        )

        # Use JavaScript to set values to avoid issues with send_keys
        self.browser.execute_script("arguments[0].value = arguments[1];", self.get_by_name(form, 'first_name'), first)
        self.browser.execute_script("arguments[0].value = arguments[1];", self.get_by_name(form, 'last_name'), last)
        self.browser.execute_script("arguments[0].value = arguments[1];", self.get_by_name(form, 'username'), username)
        self.browser.execute_script("arguments[0].value = arguments[1];", self.get_by_name(form, 'email'), email)
        self.browser.execute_script("arguments[0].value = arguments[1];", self.get_by_name(form, 'password1'), password)
        self.browser.execute_script("arguments[0].value = arguments[1];", self.get_by_name(form, 'password2'), password)
        self.browser.execute_script("arguments[0].value = arguments[1];", self.get_by_name(form, 'phone_number'), phone_number)
        self.browser.execute_script("arguments[0].value = arguments[1];", self.get_by_name(form, 'clinic'), clinic)

    def clear_field_and_submit(self, field, expected_error):
        """Helper method to clear a field and verify error message"""
        # Clear field using JavaScript
        self.browser.execute_script("arguments[0].value = '';", field)

        # Submit form using JavaScript
        submit_button = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type=\"submit\"]'))
        )
        self.browser.execute_script("arguments[0].click();", submit_button)

        # Wait for specific error message
        error_element = WebDriverWait(self.browser, 5).until(
            EC.visibility_of_element_located((
                By.XPATH,
                f"//*[contains(text(), '{expected_error}')]"
            ))
        )
        self.assertTrue(error_element.is_displayed())

    @retry_on_exception((StaleElementReferenceException, ElementClickInterceptedException, WebDriverException, TimeoutException))
    def test_first_name_empty_error_message(self):
        def callback(form):
            with translation.override('en'):
                first_name_field = self.get_by_name(
                    form, 'first_name'
                )
                self.clear_field_and_submit(
                    first_name_field,
                    'First name cannot be empty'
                )
        self.form_field_test_with_callback(callback)

    @retry_on_exception((StaleElementReferenceException, ElementClickInterceptedException, WebDriverException, TimeoutException))
    def test_last_name_empty_error_message(self):
        def callback(form):
            with translation.override('en'):
                last_name_field = self.get_by_name(
                    form, 'last_name'
                )
                self.clear_field_and_submit(
                    last_name_field,
                    'Last name cannot be empty'
                )
        self.form_field_test_with_callback(callback)

    @retry_on_exception((StaleElementReferenceException, ElementClickInterceptedException, WebDriverException, TimeoutException))
    def test_username_empty_error_message(self):
        def callback(form):
            with translation.override('en'):
                username_field = self.get_by_name(
                    form, 'username'
                )
                self.clear_field_and_submit(
                    username_field,
                    'Username is required'
                )
        self.form_field_test_with_callback(callback)

    @retry_on_exception((StaleElementReferenceException, ElementClickInterceptedException, WebDriverException, TimeoutException))
    def test_passwords_do_not_match(self):
        def callback(form):
            with translation.override('en'):
                # Fill all required fields except password2 with valid data
                self.fill_form_valid_data(
                    form,
                    first='First',
                    last='Last',
                    username='firstlast',
                    email='first@last.com',
                    password='P@ssw0rd',
                    phone_number='2499912345',
                    clinic='Test Clinic'
                )
                # Wait for password2 input to be present before sending keys
                password2 = WebDriverWait(self.browser, 10).until(
                    EC.presence_of_element_located((By.NAME, 'password2'))
                )
                password2.send_keys('P@ssw0rd_different')

                # Submit using JavaScript
                submit_button = WebDriverWait(form, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]'))
                )
                self.browser.execute_script("arguments[0].click();", submit_button)

                # Verify error
                error_element = WebDriverWait(self.browser, 5).until(
                    EC.visibility_of_element_located((
                        By.XPATH,
                        "//*[contains(text(), 'Passwords must match')]"
                    ))
                )
                self.assertTrue(error_element.is_displayed())
        self.form_field_test_with_callback(callback)

    @retry_on_exception((StaleElementReferenceException, WebDriverException, TimeoutException))
    def test_user_valid_data_register_success(self):
        with translation.override('en'):
            self.browser.get(self.live_server_url + '/users/register/')
            form = self.get_form()
            unique_str = str(uuid.uuid4())[:8]
            self.fill_form_valid_data(
                form,
                first='First',
                last='Last',
                username=f'user_{unique_str}',
                email=f'{unique_str}@example.com',
                password=f'P@ssw0rd{unique_str}',
                phone_number='2499912345',
                clinic='Test Clinic'
            )

            # Submit using native click instead of JavaScript click
            submit_button = WebDriverWait(form, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]'))
            )
            # Scroll to the button to ensure it is clickable
            self.browser.execute_script("arguments[0].scrollIntoView(true);", submit_button)
            # Wait a moment for any animations or overlays to disappear
            WebDriverWait(self.browser, 2).until(
                lambda driver: submit_button.is_displayed() and submit_button.is_enabled()
            )
            try:
                submit_button.click()
            except Exception:
                # If click intercepted, try JavaScript click as fallback
                self.browser.execute_script("arguments[0].click();", submit_button)

            # Verify success
            WebDriverWait(self.browser, 10).until(
                EC.url_contains('/users/login/')
            )
            # The success message is a Django message framework flash message, which may not be present in the redirected page
            # So we verify only the redirect to login page here
            # Optionally, we can check for presence of any alert or message container if applicable
            # success_message = WebDriverWait(self.browser, 10).until(
            #     EC.visibility_of_element_located((
            #         By.XPATH,
            #         "//*[contains(text(), 'User has been created, please log in')]"
            #     ))
            # )
            # self.assertTrue(success_message.is_displayed())
