import sys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class SelDriver:

    def __init__(self):
        self.descap = dict(DesiredCapabilities.PHANTOMJS)
        self.descap["phantomjs.page.settings.userAgent"] = (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/53 "
        "(KHTML, like Gecko) Chrome/15.0.87"
        )
        self.setup_driver()

    def setup_driver(self):
        self.driver = webdriver.PhantomJS(desired_capabilities=self.descap)
        self.driver.set_page_load_timeout(20)

    #load the url into the selenium web driver with the number of pages to scroll
    def load(self,url,pages):
        #error handling for timeout 
        try:
            self.driver.get(url)
            WebDriverWait(self.driver, 10)
            self.scroll_down(pages)
            html_page = self.driver.page_source
            return html_page
        except Exception as ex:
            print("Unexpected error: "+ex)
            #setup webdriver again. avoids bug where connections fail after first exception
            self.setup_driver()
            return

    def scroll_down(self,pages):
        for i in range(1,pages):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(4)
    
    def close(self):
         self.driver.quit()

if __name__ == "__main__":
    webdriver = SelDriver()
    if not sys.argv[1:]:
        print("Please input a starting URL.")
    else:
        print("Starting web crawling at URL: " + sys.argv[1])
        print(webdriver.load(sys.argv[1],1))
        exit()