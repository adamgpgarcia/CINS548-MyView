#!/usr/bin/python3
''' This module drives what is displayed based based on userview'''

import os
import logging
import logging.handlers
from logging.handlers import SysLogHandler
import sqlite3
import time
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By

# number of seconds to display a board
DISPLAY_TIME = 5
# Instantiate logger
# adapted from https://www.kite.com/python/docs/logging.handlers.SysLogHandler
logger = logging.getLogger('mylogger')
#logger.setLevel(logging.ERROR)
logger.setLevel(logging.DEBUG)
handler = logging.handlers.SysLogHandler(facility=SysLogHandler.LOG_DAEMON, address='/dev/log')
logger.addHandler(handler)

def getActiveList():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    #Name of MyView database
    db_file = "db.sqlite3"
    credits_page = "file:///" + dir_path + "/credits.html"
    boards = []
    conn = None
    cursor = None
    try:
        conn = sqlite3.connect(dir_path + '/' + db_file)
        cursor = conn.execute("SELECT url FROM view_viewuser WHERE connect=true")
        for row in cursor:
            boards.append(row[0])
            logger.debug("MyView: url added to rotation = %s", row[0])
    except sqlite3.Error as error:
        logger.error("MyView: %s", error)
    finally:
        boards.append(credits_page)
    return boards

def main():
    ''' main function loads urls from sqlite3 db and uses selenium to drive dakboard rotation'''
    #Set options for selenium chrome driver
    opt = Options()
    #opt.add_argument("--kiosk")
    opt.add_argument("disk-cache-size=0")
    opt.add_experimental_option("useAutomationExtension", False)
    opt.add_experimental_option("excludeSwitches", ["enable-automation"])
    #formatter = SyslogBOMFormatter(logging.BASIC_FORMAT)

    #start the browser
    driver = Chrome(options=opt)
    timeout = 1

    while True:
        boards = getActiveList()
        #display each url in boards
        for url in boards:
            print(url)
            driver.get(url)
            driver.delete_all_cookies()
            # test & remove bad links from rotation;
            # adapted from https://selenium-python.readthedocs.io/waits.html
            if driver.title != "MyView":
                try:
                    elem_present = \
                        expected_conditions.presence_of_element_located((By.ID, "dak-banner"))
                    WebDriverWait(driver, timeout).until(elem_present)
                except TimeoutException:
                    logger.error("Myview timed out loading %s", url)
                    boards.remove(url)
                finally:
                    logger.debug("MyView loaded: %s", url)
            time.sleep(DISPLAY_TIME)
    #tear down the driver
    driver.quit()



if __name__ == "__main__":
    main()
