import os, datetime, time, sys
from random import randint

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException, \
    UnexpectedAlertPresentException, WebDriverException
from pip._vendor.distlib.util import proceed

from selenium.webdriver.common.keys import Keys

class StuckException(Exception):
    pass

CHROME_DRIVER_PATH = '/Users/ishandutta2007/Downloads/chromedriver'
NETWORK_LATENCY = 0
currentYear =  2018

def login(driver):
    time.sleep(randint(3, 5) + NETWORK_LATENCY)
    try:
        driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div[1]/div/a').click()
        time.sleep(2)

        inputElement2 = driver.find_element_by_id("identifierId")
        inputElement2.send_keys('mygmail')
        inputElement2.send_keys(Keys.ENTER)
        time.sleep(5)

        inputElement2 = driver.find_element_by_xpath("//*[@id='password']/div[1]/div/div[1]/input")
        inputElement2.send_keys('mypwd')
        inputElement2.send_keys(Keys.ENTER)
        time.sleep(5)

    except NoSuchElementException as e:
        print('You are already logged in', e)

def doCG(driver, type='stcg'):
    if type == 'stcg':
        yearOfPurchase = currentYear - 1
    else:
        yearOfPurchase = currentYear - 2

    with open(type + "_data.csv") as infile:
        for ctr, fullline in enumerate(infile):
            try:
                time.sleep(4)
                driver.get('https://cleartax.in/PayTax/y2018/0/AddStcg/ThisIsShare?dateOfPurchase=01%2F04%2F'+str(yearOfPurchase)+'&dateOfSale=28%2F03%2F2018&stShareType=ListedSecurities&durationForLongTerm=TwelveMonths')
                time.sleep(2)

                linearr = fullline.split(',')
                inputDesc = linearr[1]
                inputPurchase = linearr[4]
                inputSales = linearr[7]
                print(ctr, inputDesc, inputPurchase, inputSales)

                inputDescElement = driver.find_element_by_xpath("//*[@id='stCgInstance_assetDescription']")
                inputDescElement.send_keys(inputDesc)
                time.sleep(1)

                inputSalesElement = driver.find_element_by_xpath("//*[@id='stCgInstance_grossSalesConsideration']")
                inputSalesElement.send_keys(inputSales)
                time.sleep(1)

                inputTransferElement = driver.find_element_by_xpath("//*[@id='stCgInstance_transferExpenses']")
                inputTransferElement.send_keys("40")
                time.sleep(1)

                inputPurchaseElement = driver.find_element_by_xpath("//*[@id='stCgInstance_costOfAcquisition']")
                inputPurchaseElement.send_keys(inputPurchase)
                time.sleep(1)

                sendButton = driver.find_element_by_xpath("//*[@id='main']/div[6]/form/div[2]/div/p/button")
                sendButton.click()

            except (UnexpectedAlertPresentException, WebDriverException, BaseException) as e:
                print(e)

def do():
    driver = webdriver.Chrome(CHROME_DRIVER_PATH)
    driver.get('https://cleartax.in/PayTax/y2018/0/AddStcg/ThisIsShare?dateOfPurchase=01%2F04%2F2016&dateOfSale=28%2F03%2F2018&stShareType=ListedSecurities&durationForLongTerm=TwelveMonths')
    login(driver)
    doCG(driver, type='stcg')
    doCG(driver, type='ltcg')
    driver.quit()

if __name__ == "__main__":
    do()
