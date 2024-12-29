

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import csv
import time

def setup_driver():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.implicitly_wait(10)
    return driver

def extract_vehicle_data(card, model_filter):
    details = {
        "Title": "Title not available",
        "Mileage": "Mileage not available",
        "Price": "Price not available",
        "URL": "URL not available"
    }

    try:
        title = card.find_element(By.CLASS_NAME, 'vehicle-card-title').text
        if model_filter.lower() not in title.lower():
            return None
        details["Title"] = title
    except:
        return None

    try:
        details["Mileage"] = card.find_element(By.CLASS_NAME, 'vehicle-card-highlight').text
    except:
        pass

    try:
        details["Price"] = card.find_element(By.CLASS_NAME, 'price-value').text
    except:
        pass

    try:
        details["URL"] = card.find_element(By.TAG_NAME, 'a').get_attribute('href')
    except:
        pass

    return details

def generate_pagination_urls(base_url, pages, increment=18):
    return [f"{base_url}?start={i}" for i in range(0, pages * increment, increment)]

def scroll_and_load(driver):
    """Scrolls incrementally through the page to ensure all content is loaded."""
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down by a fixed amount
        driver.execute_script("window.scrollBy(0, 2000);")
        time.sleep(1)  # Wait for new content to load

        # Calculate new scroll height and compare it with the last height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def scrape_vehicle_data(driver, url, model_filter):
    driver.get(url)
    scroll_and_load(driver)  # Ensure all content is loaded by scrolling
    vehicle_cards = driver.find_elements(By.CLASS_NAME, 'vehicle-card-details-container')
    vehicles = []
    for card in vehicle_cards:
        vehicle_data = extract_vehicle_data(card, model_filter)
        if vehicle_data:
            vehicles.append(vehicle_data)
    return vehicles

def scrape_multiple_pages_to_csv_la(output_file, model_filter, increment=18):
    driver = setup_driver()
    all_data = []

    # Hard-coded URLs and number of pages to scrape
    websites = [
        # Working
        #{"url": "https://www.hondaofstevenscreek.com/used-cars/san-jose.htm", "pages": 2},
        #{"url": "https://www.hondasancarlos.com/used-inventory/index.htm?compositeType=used", "pages": 1},
        {"url": "https://www.hondaofpasadena.com/search/used-pasadena-ca/?cy=91107&tp=used", "pages": 1},

        #{"url": "https://www.andersonhonda.com/usedcar-inventory-en-us.htm", "pages": 2},

        #{"url": "https://www.capitolhonda.com/used-vehicles/","pages": 1},


        #TOYOTA
        #{"url": "https://www.toyotapaloalto.com/used-inventory/index.htm", "pages": 2}

    ]
    try:
        for site in websites:
            urls = generate_pagination_urls(site["url"], site["pages"], increment)
            for url in urls:
                vehicle_data = scrape_vehicle_data(driver, url, model_filter)
                all_data.extend(vehicle_data)
    finally:
        driver.quit()

    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["Title", "Mileage", "Price", "URL"])
        writer.writeheader()
        writer.writerows(all_data)
