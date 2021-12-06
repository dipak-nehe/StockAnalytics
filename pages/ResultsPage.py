import re
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By

# resultpage class
class ResultsPage:
    stock_recommendation = (By.XPATH, "//*[@id=\"premium_research\"]/div/dl[1]/dd/span")
    stock_recommendation1 = (By.XPATH, "//*[@id=\"premium_research\"]/div/dl[1]/dd")
    stock_activity = (By.XPATH, "//section[@id=\"stock_activity\"]")
    stock_activity_row = (By.TAG_NAME, "dl")
    stock_last_price = (By.XPATH, "//*[@id=\"quote_ribbon_v2\"]/div[1]/div/div/p[1]")
    stock_vgm_score = (By.XPATH, "//*[@id=\"quote_ribbon_v2\"]/div[2]/div[2]/p/span[7]")

    # constructor to initialize the class
    def __init__(self, browser):
        self.browser = browser

    # extract the recommendation and return the result
    def extract_recommendation(self):
        element_extractor = self.browser.find_element(*self.stock_recommendation) or self.browser.find_element(
            *self.stock_recommendation1)
        value = element_extractor.text

        # if value is not None:
        #    print("value:" + value)
        return value

    def get_stock_price_and_calculate_percent_less_stock_trading(self):
        week_52_high = 0.0
        week_52_low = 0.0
        dividend = 0.0

        element = self.browser.find_element(*self.stock_activity)
        element_rows = element.find_elements(*self.stock_activity_row)
        for row in element_rows:
            # Form a regular expression object by passing the regex to compile methode of re module which returns
            # regex objects
            reg1 = re.compile(r'[0-9]+\.[0-9]+')
            if "52 Wk High" in row.text.replace("\n", "-"):
                week_52_high = reg1.search(row.text.replace("\n", "")).group()
                # print("week_52_high:" + week_52_high)
            elif "52 Wk Low" in row.text.replace("\n", "-"):
                week_52_low = reg1.search(row.text.replace("\n", "")).group()
                # print("week_52_low:" + week_52_low)
            elif "Dividend" in row.text.replace("\n", "-"):
                dividend = reg1.search(row.text.replace("\n", "")).group()
                # print("dividend:" + dividend)
            else:
                continue
        return week_52_high, week_52_low, dividend

    # get last price of stock from the zacks result page
    def get_stock_last_price(self):
        element = self.browser.find_element(*self.stock_last_price)
        # last_price = element.text
        reg1 = re.compile(r'[0-9]+\.[0-9]+')
        last_price = reg1.search(element.text).group()
        # print("stock last price:" + last_price)
        return last_price

    # get VGM score of the given stock
    def get_vgm_score(self):
        element = self.browser.find_element(*self.stock_vgm_score)
        stock_vgm_score = element.text
        return stock_vgm_score

    # dismiss alert
    def process_alert(self):
        # create alert object
        alert = Alert(self.browser)

        # get alert text
        print(alert.text)

        # accept the alert
        alert.accept()
