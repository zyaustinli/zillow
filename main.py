from bs4 import BeautifulSoup
import requests
import re
from selenium import webdriver
import time

zillow_link = "https://www.zillow.com/homes/for_rent/?searchQueryState=%7B%22usersSearchTerm%22%3A%22San%20Francisco%2C%20CA%22%2C%22mapBounds%22%3A%7B%22west%22%3A-122.57014361743164%2C%22east%22%3A-122.29651538256836%2C%22south%22%3A37.706060503063554%2C%22north%22%3A37.844458635052476%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22min%22%3A0%2C%22max%22%3A872627%7D%2C%22mp%22%3A%7B%22min%22%3A0%2C%22max%22%3A3000%7D%2C%22beds%22%3A%7B%22min%22%3A1%2C%22max%22%3A1%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

response = requests.get(url=zillow_link, headers=headers)
contents = response.text
soup = BeautifulSoup(contents, "html.parser")

prices = soup.find_all(attrs={"data-test": "property-card-price"})

stripped_prices = []
for price in prices:
    price = price.getText()
    if price[6] == "+":
        stripped_price = price.split("+")[0]
        stripped_prices.append(stripped_price)
    elif price[6] == "/":
        stripped_price = price.split("/")[0]
        stripped_prices.append(stripped_price)

addresses = soup.find_all(attrs={"data-test": "property-card-addr"})
stripped_addresses = []
for address in addresses:
    stripped_address = address.getText()
    if "|" in stripped_address:
        stripped_address = stripped_address.split("|")[1].strip()
    stripped_addresses.append(stripped_address)

links = soup.select(selector=".property-card-data a")

stripped_links = []
for link in links:
    stripped_link = str(link)
    stripped_link = stripped_link.split('"')[5]
    # Check if beginning has https
    https_search = re.search("^https.", stripped_link)
    if https_search:
        pass
    else:
        stripped_link = "https://www.zillow.com" + stripped_link
    stripped_links.append(stripped_link)

form_link = "https://forms.gle/kvT14NGAYPhZJo1i8"
driver = webdriver.Chrome(executable_path="/Users/denisechan/Development/chromedriver")

for i in range(len(stripped_addresses)):
    address = stripped_addresses[i]
    price = stripped_prices[i]
    link = stripped_links[i]
    driver.get(form_link)
    time.sleep(5)
    address_field = driver.find_element(by="xpath", value="//*[@id='mG61Hd']/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input")
    address_field.send_keys(address)
    time.sleep(1)
    price_field = driver.find_element(by="xpath", value="//*[@id='mG61Hd']/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input")
    price_field.send_keys(price)
    time.sleep(1)
    link_field = driver.find_element(by="xpath", value="//*[@id='mG61Hd']/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input")
    link_field.send_keys(link)
    time.sleep(1)
    submit = driver.find_element(by="xpath", value="//*[@id='mG61Hd']/div[2]/div/div[3]/div[1]/div[1]/div")
    submit.click()
    time.sleep(5)

driver.quit()
