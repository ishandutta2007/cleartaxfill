import os, datetime, time, sys
from random import randint

from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchElementException,
    ElementNotVisibleException,
    UnexpectedAlertPresentException,
    WebDriverException,
)
from pip._vendor.distlib.util import proceed

from selenium.webdriver.common.keys import Keys

CHROME_DRIVER_PATH = "/Users/ishandutta2007/.pyenv/versions/3.6.0/lib/python3.6/site-packages/instapy_chromedriver/chromedriver_mac64"
file_loc = "/Users/ishandutta2007/Desktop/"
brokerage_dmat_charges = 40
NETWORK_LATENCY = 0
current_year = 2019
skip_rows = 1
col_no_scrip = 0
col_no_tot_purchase = 4
col_no_tot_sales = 6
email = "mygmail"
password = "mypwd"


def login(driver):
    time.sleep(randint(3, 5) + NETWORK_LATENCY)
    try:
        # driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div[1]/div/a').click()
        # time.sleep(2)

        input_element_email = driver.find_element_by_id("UserName")
        input_element_email.send_keys(email)
        input_element_email.send_keys(Keys.ENTER)
        time.sleep(5)

        input_element_password = driver.find_element_by_id("Password")
        # input_element_password = driver.find_element_by_xpath("//*[@id='password']/div[1]/div/div[1]/input")
        input_element_password.send_keys(password)
        input_element_password.send_keys(Keys.ENTER)
        time.sleep(5)
    except NoSuchElementException as e:
        print("You are already logged in", e)


def doCG(driver, type="stcg"):
    if type == "stcg":
        year_of_purchase = current_year - 1
    else:
        year_of_purchase = current_year - 2

    with open(file_loc + type + "_data.csv") as infile:
        for ctr, fullline in enumerate(infile):
            if ctr < skip_rows:
                continue
            try:
                time.sleep(4)
                driver.get(
                    "https://cleartax.in/PayTax/y"
                    + str(current_year)
                    + "/0/AddStcg/ThisIsShare?dateOfPurchase=01%2F04%2F"
                    + str(yearOfPurchase)
                    + "&dateOfSale=28%2F03%2F"
                    + str(current_year)
                    + "&stShareType=ListedSecurities&durationForLongTerm=TwelveMonths"
                )
                time.sleep(2)

                line_arr = fullline.split(",")
                input_desc = line_arr[col_no_scrip]
                input_purchase = line_arr[col_no_tot_purchase]
                input_sales = line_arr[col_no_tot_sales]
                print(ctr, input_desc, input_purchase, input_sales)

                input_desc_element = driver.find_element_by_xpath(
                    "//*[@id='stCgInstance_assetDescription']"
                )
                input_desc_element.send_keys(input_desc)
                time.sleep(1)

                input_sales_element = driver.find_element_by_xpath(
                    "//*[@id='stCgInstance_grossSalesConsideration']"
                )
                input_sales_element.send_keys(input_sales)
                time.sleep(1)

                input_transfer_element = driver.find_element_by_xpath(
                    "//*[@id='stCgInstance_transferExpenses']"
                )
                input_transfer_element.send_keys(str(brokerage_dmat_charges))
                time.sleep(1)

                input_purchase_element = driver.find_element_by_xpath(
                    "//*[@id='stCgInstance_costOfAcquisition']"
                )
                input_purchase_element.send_keys(input_purchase)
                time.sleep(1)

                send_button = driver.find_element_by_xpath(
                    "//*[@id='main']/div[6]/form/div[2]/div/p/button"
                )
                send_button.click()

            except (
                UnexpectedAlertPresentException,
                WebDriverException,
                BaseException,
            ) as e:
                print(e)


def do():
    driver = webdriver.Chrome(CHROME_DRIVER_PATH)
    driver.get(
        "https://cleartax.in/PayTax/y"
        + str(current_year)
        + "/0/AddStcg/ThisIsShare?dateOfPurchase=01%2F04%2F"
        + str(current_year - 2)
        + "&dateOfSale=28%2F03%2F"
        + str(current_year)
        + "&stShareType=ListedSecurities&durationForLongTerm=TwelveMonths"
    )
    login(driver)
    doCG(driver, type="stcg")
    doCG(driver, type="ltcg")
    driver.quit()


if __name__ == "__main__":
    do()
