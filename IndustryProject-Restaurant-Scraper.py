import pandas
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument("--headless") 

from bs4 import BeautifulSoup

# This is the website to scrap for this industry project
# https://whitehart.tablemenu.co/inhouse_order

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://whitehart.tablemenu.co/inhouse_order")

# Expand food descriptions by clicking on 'more'
anchors = driver.find_elements(By.CSS_SELECTOR, ".more")
for anchor in anchors:
    script = "arguments[0].click();"
    driver.execute_script(script, anchor)
    
#Wait for the whole page to load before driver quits and chrome closes.
time.sleep(15)

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

foodTypes, productsName, descriptionList, priceList, veganList, spicyList = [], [], [], [], [], []
foodCategories = soup.find_all('div', class_ = 'category_box')
for category in foodCategories:
    foodType = category.find('div', class_ = 'cat_heading invert_dark').text.strip().capitalize()
    
    products = category.find_all('h3', class_ = 'product_name')
    for product in products:
        productsName.append(product['title'].strip().title())
        foodTypes.append(foodType)
        
        images = product.find_all('img', class_ = 'img-popover img img-circle')

        #Checking if both vegan and spicy are not present on a specific dish
        if len(images) == 0:
            veganList.append('')
            spicyList.append('')
          
        else:
            spicy, vegan = 0, 0
            for image in images:
                temp = image['data-content']
                
                if 'Vegetarian' in temp:
                    break
                if 'Vegan' in temp:
                    vegan = 1
                    veganList.append(temp)
                elif 'Spicy' or 'Mild' in temp:
                    spicy = 1
                    spicyList.append(temp)
            if spicy == 0:
                spicyList.append('')
            if vegan == 0:
                veganList.append('')
                    
    descriptions = category.find_all('p', class_='minimize')
    for description in descriptions:
        descriptionList.append(description.get_text(strip=True).replace('...More', '').replace('Less', '').replace('\n', ' '))
    
    prices = category.find_all('span', class_ = 'menu-price dark')
    for price in prices:
        priceList.append(price.text.strip())
    
data = pandas.DataFrame(zip(productsName, descriptionList, priceList, foodTypes, veganList, spicyList), columns = ['Product', 'Description', 'Price', 'Food Type', 'Vegan', 'Spicy'])

data.to_csv('IndustryProject-Restaurant-Processed.csv', index=False)