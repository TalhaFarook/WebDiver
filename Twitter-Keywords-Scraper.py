from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains

# Set up your own custom web driver with your local data in it (you are logged in to their twitter account)
service = Service(executable_path = r"C:\Users\USER\Documents\ChromeDriver\chromedriver.exe")
option = Options()

chrome_options = webdriver.ChromeOptions()
option.add_experimental_option("debuggerAddress", "localhost:9222")
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(options = chrome_options)

from bs4 import BeautifulSoup
import time

from collections import OrderedDict
import pandas
pandas.set_option('display.max_colwidth', None)
pandas.set_option('display.max_rows', None)

# URl encode the users search query to put in the url
import urllib.parse

def encodeURL(query):
    return urllib.parse.quote(query)

def twitter(query, num): 
    # Preparing the URL for it
    url = 'https://twitter.com/search?q=' + encodeURL(query) + '&f=live'

    # Getting the web driver with custom options and establishing a connection with the prepared URL
    driver = webdriver.Chrome(service=service, options=option)
    try:
        driver.get(url)

        # Wait for the website to load initially
        time.sleep(3)

        temp, flat, htmlLinks = [], [], []
        # This range is set because a scrolling action will be taken by the chrome driver, as the posts load dynamically when you reach the end of the page. Decreasing it will result in fewer searches.
        for _ in range(1, num):
            # Deliberate sleep is added because the posts are loaded dynamically, so the script has to wait for the next set of posts to load when you reach the bottom.
            time.sleep(1)

            # Scrolling action performed here
            driver.execute_script("window.scrollBy(0, 2000);")

            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            # HTML of all the links are taken from the website
            temp.append(soup.find_all('div', class_='css-1dbjc4n r-18u37iz r-1q142lx'))

            # Flatten the list 
            flat = [row for rows in temp for row in rows]

            # There are duplicates, because the scroller option jumps when it reaches the end and next set of tweets are loaded. Removing the duplicates by OrderedDict, which makes sure that we retain the original order of tweets/links
            htmlLinks = list(OrderedDict.fromkeys(flat))

            # Checking the total amount of HTMl of links received (There are repetitions though!)
            total = sum(len(row) for row in htmlLinks)

            if total >= num + int(num/2):  
                break

        # Creating a list of links extracted from the HTML
        links, counter = [], 0
        for link in htmlLinks:
            try:
                if link.find('a') is not None:
                    counter += 1
                    if counter <= num:
                        links.append('https://twitter.com' + link.find('a')['href'])
                    else:
                        break
        
            except Exception as e:
                print(f"An error occurred while processing link: {e}")

        # Close the WebDriver
        driver.quit()

        # Extact data from each facebook page retrieved
        driver = webdriver.Chrome(service=service, options=option)

        nameList, urlList = [], []
        for link in links:
            try:
                driver.get(link)

                wait = WebDriverWait(driver, 10)
                elements = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.css-1dbjc4n.r-vacyoi.r-ttdzmv')))

                html = driver.page_source
                soup = BeautifulSoup(html, 'html.parser')

                nameHTML = soup.find_all('span', class_='css-901oao css-16my406 css-1hf3ou5 r-poiln3 r-bcqeeo r-qvutc0')
                if nameHTML is not None:
                    nameList.append(nameHTML[1].text.strip())
                else:
                    nameList.append('')

                urlList.append(link)

            except Exception as e:
                print(f"An error occurred while processing link: {e}")

        # Close the WebDriver
        driver.quit()

        # Create a DataFrame from the lists and save it into a CSV format
        output = pandas.DataFrame({'User Name': nameList, 'Post URL': urlList})
        
        output.to_csv('Twitter-Unprocessed.csv', index=False)

    except Exception as e:
        print(f"An error occurred while running the script: {e}")

keyword = ''
maxSearch = 0

twitter(keyword, maxSearch)
