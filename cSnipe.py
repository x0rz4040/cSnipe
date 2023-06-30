## import all the necessary modules. Make sure you have them.
## modules can be installed using 
from selenium import webdriver
from selenium.webdriver.common.by import By
from send_email import test_sendmail
import time
import unidecode


## parameters blah
#NON_ZERO_ZIP = str(2351)
#YOUR_ZIPCODE = NON_ZERO_ZIP.zfill(4)
YOUR_ZIPCODE = input("Enter your zip code: ")
SEARCH = input("What do you want to search for? ")
RADIUS = input("Enter max amount of miles you're willing to travel: ")
MAX_PRICE = input("Enter the max price you're willing to pay for an item: ")
WAIT = int(input("How often should we refresh the search? "))
ITEMS_TO_LOOK =  input("What keywords are you looking for? ")
CITY = input("What city are you in? LOWERCASE ONLY NO SPACES ")

## generate the url for the above parameters for your area.
## here its generated for hartford area but you might want to change based on
## your location. Open craiglist and it will direct you the relevant subdomain
##url ='https://boston.craigslist.org/search/fua?sort=date&query=chair&search_distance=60'

oldUrl='https://newyork.craigslist.org/d/for-sale/search/sss?sort=date&max_price=300&postal=10018&query=chair&search_distance=10'
newUrl= 'https://'+CITY+'.'+'craigslist.org/d/for-sale/search/sss?sort=data&maxprice='+MAX_PRICE+'&postal='+YOUR_ZIPCODE+'&query='+SEARCH+"&search_distance="+RADIUS
## intantiate a firefox browser instance
driver=webdriver.Firefox()
## load the url
driver.get(newUrl)

## declare and empty list to keep the items. This will also come in handy to check items
## that are newly added
items = []

## get all the items on the first page. Not concerned about the other pages
results = driver.find_elements(By.CSS_SELECTOR,'.result-row')

## iterate through the results to find the text
for result in results:
    a = results[0].find_element_by_css_selector('.result-info')
    items.append(unidecode(a.find_element_by_tag_name('a').text))

## in a while loop. This makes it an infinite loop
## LOGIC - keep checking every WAIT minutes and find new items that are added
## if any new item found, email it to the user
## else sleep.
while True:
    driver.get(newUrl)
    time.sleep(5)
    results = driver.find_elements(By.CSS_SELECTOR,'.result-row')
    for result in results:
        a = results[0].find_element_by_css_selector('.result-info')
        text = unidecode(a.find_element_by_tag_name('a').text)
        if (text not in items) and (any(ext.lower().strip() in text.lower().strip() for ext in ITEMS_TO_LOOK)):
            items.append(text)
            test_sendmail(text)
            
    time.sleep(WAIT*60)## sleep