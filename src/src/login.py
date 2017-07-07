
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from .core import BasePage




class login(BasePage):

    def login_UserName(self, UserName):
        self.login_UserName_loc = (By.ID, self.login_UserName_loc_)
        self.find_element(*self.login_UserName_loc).clear()
        self.find_element(*self.login_UserName_loc).send_keys(UserName)

    def login_Password(self, Password):
        self.login_Password_loc = (By.ID, self.login_Password_loc_)
        try:
            self.find_element(*self.login_Password_loc).clear()
            self.find_element(*self.login_Password_loc).send_keys(Password)
        except:
            self.driver.find_element_by_tag_name('body').send_keys(Keys.TAB + Password)

    def login_SignIn(self):
        self.login_SignIn_loc = (By.CLASS_NAME, self.login_SignIn_loc_)
        self.find_element(*self.login_SignIn_loc).click()

    def user_Login(self, UserName, Password):
        self.open()
        self.login_UserName(UserName)
        self.login_Password(Password)
        self.login_SignIn()
        sleep(1)

    login_error_hint_loc = (By.CLASS_NAME, "error-container")
    login_success_hint_loc = (By.LINK_TEXT, "Log Off")

    def login_error_hint(self):
        return self.find_element(*self.login_error_hint_loc).text

    def login_success(self):
        return self.find_element(*self.login_success_hint_loc).text