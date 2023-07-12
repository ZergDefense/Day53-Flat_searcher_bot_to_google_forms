from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

ZILLOW_LINK = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3Anull%2C%22mapBounds%22%3A%7B%22west%22%3A-122.56276167822266%2C%22east%22%3A-122.30389632177734%2C%22south%22%3A37.69261345230467%2C%22north%22%3A37.857877098316834%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D"
CHROME_DRIVER_PATH = "C:\ChromeDriver-for-Selenium\chromedriver.exe"
GOOGLE_FORM_LINK = "https://docs.google.com/forms/d/e/1FAIpQLSf-2k7TAzcf-Ai06AdrIwKn87BvzT63sDS6mJ47xSDlocVD2w/viewform"

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
    "accept-language": "hu,en-US;q=0.9,en;q=0.8,hu-HU;q=0.7,pt;q=0.6,de;q=0.5"
}

response = requests.get(ZILLOW_LINK, headers=headers)
zillow_page = response.text
print(response.status_code)

soup = BeautifulSoup(zillow_page, "html.parser")

articles = soup.find_all('article', class_='property-card')
print(f"all_link_elements: {articles}")

all_links = []
for article in articles:
    link = article.find_next('a', class_='property-card-link')

    if link['href'].startswith("https://www.zillow.com"):
        all_links.append(link['href'])
    else:
        all_links.append("https://www.zillow.com" + link['href'])

print(f"all_links: {all_links}")

all_address_elements = soup.find_all('address', {'data-test': 'property-card-addr'})
all_addresses = [address.get_text().split(" | ")[-1] for address in all_address_elements]
print(f"all_addresses: {all_addresses}")

all_price_elements = soup.find_all('span', {'data-test': 'property-card-price'})
all_prices = [price.get_text().split("+")[0] for price in all_price_elements if "$" in price.text]
all_prices = [price.split("/")[0] for price in all_prices]
print(f"all_prices: {all_prices}")

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
service = Service(executable_path=CHROME_DRIVER_PATH)
driver = webdriver.Chrome(service=service, options=chrome_options)

for n in range(len(all_links)):
    driver.get(GOOGLE_FORM_LINK)

    time.sleep(2)
    address = driver.find_element(by=By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price = driver.find_element(by=By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link = driver.find_element(by=By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    submit_button = driver.find_element(by=By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div')

    address.send_keys(all_addresses[n])
    price.send_keys(all_prices[n])
    link.send_keys(all_links[n])
    submit_button.click()
