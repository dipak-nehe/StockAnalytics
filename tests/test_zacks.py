import pytest
from selenium.common.exceptions import NoSuchElementException
from pages.HomePage import HomePage
from pages.ResultsPage import ResultsPage
from commonModules import Utility
from commonModules import smsModule

# Global dictionary to store the zack's recommendations
stockRating = {}


@pytest.mark.parametrize('stock', Utility.read_excel(Utility.pathString))
def test_stocks(browser, stock):
    global stockRating
    print("Getting stock ratings for:" + stock + " from Zack's")
    search_page = HomePage(browser)
    result_page = ResultsPage(browser)
    title = search_page.load_home_page()
    print(title)
    search_page.search_stock(stock)

    try:
        # result_page.process_alert()
        stock_rating = result_page.extract_recommendation()
        (week_52_high, week_52_low, dividend) = result_page.get_stock_price_and_calculate_percent_less_stock_trading()
        stock_last_price = result_page.get_stock_last_price()
        stock_vgm_score = result_page.get_vgm_score()
        percent_deviation_from_52_week_High = Utility.calculate_percent_less_or_more_the_stock_trading(
            stock_last_price, week_52_high, week_52_low)
        if stock_rating in ["1", "2"] and stock_vgm_score in ["A", "B"] and percent_deviation_from_52_week_High < -10.00:
            body = "Zack's rating {} VGM score {} last pr {} with 52_wk_hgh {} and 52_wk_lw {} with dividend {} " \
                   "having {}% deviation".format(stock_rating, stock_vgm_score, stock_last_price, week_52_high,
                                                 week_52_low, dividend,
                                                 percent_deviation_from_52_week_High)
            # smsModule.send_sms(stock, stock_rating)
            smsModule.send_sms(stock, body)
        stockRating.update({stock: stock_rating})
    except NoSuchElementException as err:
        print("Error:{0}".format(err))

    # stock_rating = stock_rating)
    # assert stock_rating in ["1"  , "2", "3", "4", "5", "NA"]


def test_create_excel_write_stock_rating():
    global stockRating
    Utility.write_excel(stockRating)
