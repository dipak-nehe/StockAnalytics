from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By


class HomePage:
    url = "https://www.zacks.com/"
    search_input_for_stocks = (By.XPATH, "//*[@id=\"search-q\"]")

    # constructor to initialize the class
    def __init__(self, browser):
        self.browser = browser

    # load the Zacks home page
    def load_home_page(self):
        self.browser.get(self.url)
        return self.browser.title

    # Enter stock to search and press return key
    def search_stock(self, stock):
        try:
            search_input_element = self.browser.find_element(*self.search_input_for_stocks)
            search_input_element.send_keys(stock + Keys.RETURN)
        except NoSuchElementException:
            print("element not present")
