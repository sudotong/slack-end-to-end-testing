import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

class SeleniumLib(object):


    def wait_for_id(self, object_id):
        driver = self.driver
        try:
            element = WebDriverWait(driver, self.wait_time).until(
                EC.presence_of_element_located((By.ID, object_id))
            )
        except TimeoutException:
            print 'loading took to much time for: ', object_id
            assert False

    def wait_for_xpath(self, path, should_assert=False):
        driver = self.driver
        try:
            element = WebDriverWait(driver, self.wait_time).until(
                EC.presence_of_element_located((By.XPATH, path))
            )
            return True
        except TimeoutException:
            print 'loading took to much time for: ', path
            #if should_assert:
            #    assert False # should this assert?
            return False

    def wait_for_css_path(self, path, should_assert=False):
        driver = self.driver
        try:
            element = WebDriverWait(driver, self.wait_time).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, path))
            )
            driver.find_element_by_css_selector(path)
            return True
        except TimeoutException:
            print 'loading took to much time for: ', path
            #if should_assert:
            assert False # should this assert?
            return False

    def wait_for_css_path_to_be_visible(self, path, should_assert=False):
        driver = self.driver
        try:
            element = WebDriverWait(driver, self.wait_time).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, path))
            )
            driver.find_element_by_css_selector(path)
            return True
        except TimeoutException:
            print 'loading took to much time for: ', path
            #if should_assert:
            assert False # should this assert?
            return False

    def wait_for_id_to_be_clickable(self, object_id):
        driver = self.driver
        try:
            element = WebDriverWait(driver, self.wait_time).until(
                EC.element_to_be_clickable((By.ID, object_id))
            )
            time.sleep(1)
            driver.find_element_by_id(object_id).click()
        except TimeoutException:
            print 'loading took too much time for: ', object_id
            assert False

    def wait_for_xpath_to_be_clickable(self, object_path, should_assert=True):
        driver = self.driver
        try:
            element = WebDriverWait(driver, self.wait_time).until(
                EC.element_to_be_clickable((By.XPATH, object_path))
            )
            time.sleep(1)
            driver.find_element_by_xpath(object_path).click()
        except TimeoutException:
            print 'loading took too much time for: ', object_path
            if should_assert:
                assert False

    def wait_for_css_path_to_be_clickable(self, object_path):
        driver = self.driver
        try:
            element = WebDriverWait(driver, self.wait_time).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, object_path))
            )
            time.sleep(1)
            driver.find_element_by_css_selector(object_path).click()
        except TimeoutException:
            print 'loading took too much time for: ', object_path
            assert False

    def wait_for_text_in_xpath(self, path, wait_text, should_assert=True):
        driver = self.driver
        try:
            element = WebDriverWait(driver, self.wait_time).until(
                EC.text_to_be_present_in_element((By.XPATH, path), wait_text)
            )
        except TimeoutException:
            print "loading took too much time for: ", wait_text, " in ", path
            if should_assert:
                assert False

    def wait_for_text_in_css_path(self, path, wait_text, should_assert=True):
        driver = self.driver
        try:
            element = WebDriverWait(driver, self.wait_time).until(
                EC.text_to_be_present_in_element((By.CSS_SELECTOR, path), wait_text)
            )
        except TimeoutException:
            print "loading took too much time for: ", wait_text, " in ", path
            if should_assert:
                assert False

    def get_attribute_in_css_path(self, path, attribute):
        driver = self.driver
        try:
            element = WebDriverWait(driver, self.wait_time).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, path))
            )
            time.sleep(1)
            return element.get_attribute(attribute)
        except TimeoutException:
            print 'loading took too much time for: ', object_path
            assert False

    def __init__(self, driver, wait_time=10):
        self.driver = driver
        self.wait_time = wait_time
