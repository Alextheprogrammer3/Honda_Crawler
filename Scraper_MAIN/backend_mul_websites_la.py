import csv
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_driver():
    """Set up and return the Chrome WebDriver."""
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.implicitly_wait(10)
    return driver

def extract_vehicle_data(card, model_filter):
    """Extract vehicle data from a single vehicle card."""
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
    except Exception as e:
        logger.error(f"Error extracting title: {e}")

    try:
        details["Mileage"] = card.find_element(By.CLASS_NAME, 'vehicle-card-highlight').text
    except Exception as e:
        logger.warning(f"Error extracting mileage: {e}")

    try:
        details["Price"] = card.find_element(By.CLASS_NAME, 'price-value').text
    except Exception as e:
        logger.warning(f"Error extracting price: {e}")

    try:
        details["URL"] = card.find_element(By.TAG_NAME, 'a').get_attribute('href')
    except Exception as e:
        logger.warning(f"Error extracting URL: {e}")

    return details

def generate_pagination_urls(base_url, pages, increment=18):
    """Generate URLs for paginated listings."""
    return [f"{base_url}?start={i}" for i in range(0, pages * increment, increment)]

def scroll_and_load(driver):
    """Scrolls incrementally through the page to ensure all content is loaded."""
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollBy(0, 2000);")
        time.sleep(1)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def scrape_vehicle_data(driver, url, model_filter):
    """Scrape vehicle data from a single page URL."""
    driver.get(url)
    scroll_and_load(driver)  # Ensure all content is loaded by scrolling
    vehicle_cards = driver.find_elements(By.CLASS_NAME, 'vehicle-card-details-container')
    vehicles = []
    for card in vehicle_cards:
        vehicle_data = extract_vehicle_data(card, model_filter)
        if vehicle_data:
            vehicles.append(vehicle_data)
    return vehicles

def scrape_dealership_data(website, model_filter, increment=18):
    """Scrape multiple pages from a single dealership's website."""
    all_data = []
    urls = generate_pagination_urls(website["url"], website["pages"], increment)
    driver = setup_driver()

    try:
        for url in urls:
            logger.info(f"Scraping {url}")
            vehicle_data = scrape_vehicle_data(driver, url, model_filter)
            all_data.extend(vehicle_data)
    except Exception as e:
        logger.error(f"Error scraping {website['url']}: {e}")
    finally:
        driver.quit()

    return all_data

def scrape_multiple_sites_to_csv(output_file, model_filter, increment=18):
    """Scrape vehicle data from multiple websites and save it to a CSV file."""
    websites = [
        {"url": "https://www.hondaofpasadena.com/search/used-pasadena-ca/?cy=91107&tp=used", "pages": 1},
        # Add other websites here
    ]

    all_data = []
    for site in websites:
        site_data = scrape_dealership_data(site, model_filter, increment)
        all_data.extend(site_data)

    # Save the results to a CSV file
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["Title", "Mileage", "Price", "URL"])
        writer.writeheader()
        writer.writerows(all_data)
    logger.info(f"Data successfully written to {output_file}")

# Example usage:
if __name__ == "__main__":
    model_filter = "Civic"  # Change this to the car model you're looking for
    output_file = "vehicle_data.csv"
    scrape_multiple_sites_to_csv(output_file, model_filter)
