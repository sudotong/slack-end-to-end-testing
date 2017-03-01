from common import SeleniumLib
from selenium import webdriver
import time

class DriverFactory(object):

    def __init__(self, wait_time=20):
        self.drivers = []
        self.wait_time = wait_time

    def get_driver(self, use_old=True):
        # use_old: set to False if you always want a new driver
        if use_old and len(self.drivers) >= 1:
            print 'returning existing driver'
            return self.drivers[0]

        profile = webdriver.FirefoxProfile()
        #profile.add_extension(extension='../resources/firebug-2.0.18-fx.xpi')
        #profile.set_preference("extensions.firebug.currentVersion", "2.0.18")

        #firepath is super helpful for getting CSS and X paths
        #profile.add_extension(extension='../resources/firepath-0.9.7.1-fx.xpi')
        #profile.set_preference("browser.privatebrowsing.autostart", True)

        driver = webdriver.Firefox(firefox_profile=profile)

        #in case you want to run headless
        #self.driver = webdriver.PhantomJS()
        #self.driver.set_window_size(1120, 550)

        driver.implicitly_wait(self.wait_time)
        self.drivers.append(driver)
        return driver

    def terminate_drivers(self):
        for driver in self.drivers:
            driver.close()
            driver.quit()
