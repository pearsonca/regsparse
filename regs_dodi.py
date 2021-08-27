from selenium.webdriver import Chrome, ChromeOptions

from bs4 import BeautifulSoup, SoupStrainer
import re

import sys

chrdriver, downloaddir = sys.argv[1:]

pat = re.compile("\.pdf")
httpat = re.compile("^http")
rooturl = 'https://www.esd.whs.mil'

def extractor(html):
    for link in BeautifulSoup(html_source, parse_only=SoupStrainer('a')):
        if (link.has_attr('href')) and (pat.search(link['href']) is not None):
            if httpat.search(link['href']) is None:
                yield rooturl + link['href']
            else:
                yield link['href']

options = ChromeOptions()
options.add_experimental_option("prefs", {
  "download.default_directory": downloaddir,
  "download.prompt_for_download": False,
  "download.directory_upgrade": True,
  "plugins.always_open_pdf_externally": True,
  "safebrowsing.enabled": True
})

browser = Chrome(executable_path='./chromedriver', options=options)
browser.get(rooturl + "/directives/issuances/dodi")
html_source = browser.page_source
srcs = [l for l in extractor(html_source)]
for pdf in srcs:
    browser.get(pdf)

browser.quit()
