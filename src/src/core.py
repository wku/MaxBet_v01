
from asyncio.log import logger

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.events import EventFiringWebDriver, AbstractEventListener
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile




class MyListener(AbstractEventListener):

    def before_navigate_to(self, url, driver):
        pass

    def after_navigate_to(self, url, driver):
        pass

    def before_change_value_of(self, element, driver):
        pass

    def after_change_value_of(self, element, driver):
        pass

    def before_navigate_back(self, driver):
        pass

    def after_navigate_back(self, driver):
        pass

    def before_navigate_forward(self, driver):
        pass

    def after_navigate_forward(self, driver):
        pass

    def before_find(self, by, value, driver):
        pass

    def after_find(self, by, value, driver):
        pass

    def before_click(self, element, driver):
        pass

    def after_click(self, element, driver):
        pass

    def before_execute_script(self, script, driver):
        pass

    def after_execute_script(self, script, driver):
        pass

    def before_close(self, driver):
        pass

    def after_close(self, driver):
        pass

    def before_quit(self, driver):
        pass

    def after_quit(self, driver):
        pass

    def on_exception(self, exception, driver):
        pass


class BasePage(object):

    def __init__(self, login_UserName_loc_, login_Password_loc_, login_SignIn_loc_, port=0, server=True):
        self.server = server
        self.port = port
        self.login_UserName_loc_ = login_UserName_loc_
        self.login_Password_loc_ = login_Password_loc_
        self.login_SignIn_loc_ = login_SignIn_loc_
        self.timeout = 30
        self.createNew()

    def createNew(self):
        if self.server:
            desired_cap = { 'platform': "Windows 10", 'browserName': "chrome", 'version': "54.0" }
            self.driver_ = webdriver.Remote(command_executor='http://localhost:4444/wd/hub',   desired_capabilities=desired_cap)
            self.driver = EventFiringWebDriver(self.driver_, MyListener())
        else:

            if True:
                chrome_options = webdriver.ChromeOptions()
                chrome_options.add_argument('--no-sandbox')

                d = DesiredCapabilities.CHROME
                d['loggingPrefs'] = {'browser': 'ALL'}

                service_args = ['--verbose', '--no-sandbox', "--log-path=./qc1.log"]
                service_log_path = 'chromedriver.log'
                self.driver_ = webdriver.Chrome('./src/chromedriver', service_args=service_args, service_log_path=service_log_path, chrome_options=chrome_options, desired_capabilities=d)
                self.driver = EventFiringWebDriver(self.driver_, MyListener())

            if False:
                firefox_profile = webdriver.FirefoxProfile()
                firefox_profile.set_preference('permissions.default.stylesheet', 2)
                firefox_profile.set_preference('permissions.default.image', 2)
                firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
                driver = webdriver.Firefox(firefox_profile=firefox_profile)
                # Disable CSS
                firefox_profile.set_preference('permissions.default.stylesheet', 2)
                # Disable images
                firefox_profile.set_preference('permissions.default.image', 2)
                # Disable JavaScript
                firefox_profile.set_preference('javascript.enabled', False)
                # Disable Flash
                firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
                firefox_capabilities = DesiredCapabilities.FIREFOX
                firefox_capabilities['marionette'] = True
                firefox_capabilities['binary'] = '/usr/bin/firefox'
                self.driver_  = webdriver.Firefox(firefox_profile=firefox_profile, capabilities=firefox_capabilities)




    def _open(self, url):
        url = url
        self.driver.get(url)
        assert self.on_page(), 'Did not land on %s' % url

    def on_page(self):
        return self.driver.current_url == (self.url)

    def script(self, src):
        return self.driver.execute_script(src)

    def open(self):
        self._open(self.url)

    def find_element(self, *loc):
        try:
            return self.driver.find_element(*loc)
        except AttributeError as e:
            logger.error(str(e))
            print('Страница не найдена %s' % e)

    def find_elements(self, *loc):
        try:
            if len(self.driver.find_elemnts(*loc)):
                return self.driver.find_elemnts(*loc)
        except AttributeError as e:
            logger.error(str(e))
            print('Страница не найдена %s' % e)

    def click_button(self, *loc):
        try:
            self.find_element(*loc).click()
        except AttributeError as e:
            logger.error(str(e))
            print('Страница не найдена %s' % e)

    def wait_activity(self, *loc):
        try:
            return self.driver.wait_activity(*loc)
        except AttributeError as e:
            logger.error(str(e))
            print('Страница не найдена %s' % e)

    def execute_script(self, *loc):
        try:
            return self.driver.execute_script(*loc)
        except AttributeError as e:
            logger.error(str(e))
            print('except execute_script %s' % e)
            return None


    def execute_async_script(self, *loc):
        try:
            self.driver.set_script_timeout(60) #120
            data =  self.driver.execute_async_script(*loc)
        except AttributeError as e:
            logger.error(str(e))
            print('except execute_async_script %s' % e)
            data =  None
        return data

    def swipe(self, *loc):
        try:
            return self.driver.swipe(*loc)
        except AttributeError as e:
            logger.error(str(e))
            print('ошибка эмуляции мобильника %s' % e)

    def keyevent(self, *loc):
        self.driver.keyevent(*loc)

    def maximize_window(self):
        self.driver.maximize_window()

    def current_url(self):
        return self.driver.current_url


    def exit(self):
        self.driver.quit()

    def close(self):
        self.driver.close()
