#!/usr/bin/python3
# Author: Nathan Tisdale
# Purpose: proof of concept: use selenium to drive dakboard rotation
import time
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
import logging
import logging.handlers
from logging.handlers import SysLogHandler

# Instantiate logger: adapted from https://www.kite.com/python/docs/logging.handlers.SysLogHandler
logger = logging.getLogger('mylogger')
logger.setLevel(logging.ERROR)

handler = logging.handlers.SysLogHandler(facility=SysLogHandler.LOG_DAEMON, address='/dev/log')
logger.addHandler(handler)

#boards list can be imported from file or db
boards = [
   "file:///opt/myview/credits.html",
   "https://www.dakboard.com/app?p=26c8cd461ee43fe0c48bf4dcecd14ff2",
   "https://tisdale.info/nothing/to/see/here"
]

#Set options for selenium chrome driver
opt = Options()
#opt.add_argument("--kiosk")
opt.add_experimental_option("useAutomationExtension", False)
opt.add_experimental_option("excludeSwitches",["enable-automation"])
#formatter = SyslogBOMFormatter(logging.BASIC_FORMAT)

#start the browser
driver = Chrome(options=opt)
timeout = 1

while (True):
   #display each url in boards
   for url in boards:
      driver.get(url)
      # test & remove bad links from rotation; adapted from https://selenium-python.readthedocs.io/waits.html
      if (driver.title!="MyView"):
         try:
            elem_present = expected_conditions.presence_of_element_located((By.ID, "dak-banner"))
            WebDriverWait(driver,timeout).until(elem_present)
         except TimeoutException:
            logger.error("Myview timed out loading " + url)
            boards.remove(url)
         finally:
            logger.debug("MyView loaded: " + url)
      time.sleep(5)
#tear down the driver
driver.quit()
