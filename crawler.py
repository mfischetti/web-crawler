import sys
import time
from collections import deque
from bs4 import BeautifulSoup
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
            print("Unexpected error: "+str(ex))
            #setup webdriver again. avoids bug where connections fail after first exception
            self.setup_driver()
            return

    def scroll_down(self,pages):
        for i in range(1,pages):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(4)
    
    def close(self):
         self.driver.quit()


class UrlScraper:
    """
    maxdepth -> the maximum depth the scraper can crawl from starting url 
    depth -> current depth the scraper is at 
    pages -> maximum number of pages the web driver will to scroll

    """
    def __init__(self, maxdepth, pages):
        self.maxdepth = maxdepth
        self.depth = 0
        self.pages = pages
        self.seldriver = SelDriver()
        self.links_to_crawl = deque([])
        self.already_crawled = []

    def crawl(self,url,curr_depth):
        self.links_to_crawl.append([url,curr_depth])
        #bfs traversial - urls are added in order by depth
        while len(self.links_to_crawl):
            new_url = self.links_to_crawl.popleft()
            curr_depth = new_url[1]
            self.already_crawled.append(new_url[0])
            html_page = self.seldriver.load(new_url[0],self.pages)
            for url in self.parse_url(html_page,curr_depth):
                print(url)

    def parse_url(self,html_page,curr_depth):
        curr_depth += 1
        #stop adding urls once we reached our max depth
        if curr_depth > self.maxdepth:
            return
        try:
            soup = BeautifulSoup(html_page, "lxml")
        except Exception as ex:
            print("Unexpected error: "+str(ex))
            return          
        for anchor in soup.findAll('a', href=True):
            link = anchor['href']
            #grab additinal links and add them to queue for fruther crawling
            if (link.startswith("https://") and link not in self.links_to_crawl and
            link not in self.already_crawled):
                self.links_to_crawl.append([link,curr_depth])
                yield link

    def finish_scraping(self):
        self.seldriver.close()
    
if __name__ == "__main__":
    spider = UrlScraper(2,1)
    if not sys.argv[1:]:
        print("Please input a starting URL.")
    else:
        print("Starting web crawling at URL: " + sys.argv[1])
        spider.crawl(sys.argv[1],0)
        print("Web crawling complete.")
    spider.finish_scraping()
    exit()