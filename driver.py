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

#boards list can be imported from file or db
boards = [
   "file:///opt/myview/credits.html",
   "https://www.dakboard.com/app?p=26c8cd461ee43fe0c48bf4dcecd14ff2"
]

#Set options for selenium chrome driver
opt = Options()
#opt.add_argument("--kiosk")
opt.add_experimental_option("useAutomationExtension", False)
opt.add_experimental_option("excludeSwitches",["enable-automation"])

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
            print("Exception: Page load timed out")
            boards.remove(url)
         finally:
            print("page loaded")
      time.sleep(5)
#tear down the driver
driver.quit()
