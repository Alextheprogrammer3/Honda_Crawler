# Honda_Crawler

## Project Overview

**Honda_Crawler** is an advanced automated web scraping tool built using Python and Selenium WebDriver, designed to extract comprehensive vehicle data from multiple dealership websites. The scraper navigates through paginated listings, dynamically loads content, and filters results by car model. Extracted vehicle details—such as title, mileage, price, and URL—are stored in a CSV file for easy analysis and reporting.

## Key Features

- **Dynamic Content Handling**: Utilizes Selenium to interact with JavaScript-rendered pages, ensuring that content is fully loaded before extraction.
- **Pagination Support**: Automatically generates URLs for paginated vehicle listings and processes each page to gather all available data.
- **Model-Based Filtering**: Users can filter vehicles based on specific car models to focus on relevant data.
- **Efficient Data Extraction**: Scrapes critical vehicle details including:
  - **Title**: The vehicle model and variant.
  - **Mileage**: The vehicle's total distance traveled.
  - **Price**: The listed price of the vehicle.
  - **URL**: The direct link to the vehicle listing.
- **Data Storage**: All extracted data is saved in CSV format, making it accessible for further analysis and insights.

## Technical Stack

- **Python**: The primary programming language used for the web scraping and automation logic.
- **Selenium**: Web automation tool that interacts with the web pages, simulating a real user to handle dynamic content.
- **Webdriver Manager**: Manages browser drivers for Selenium, ensuring compatibility with different browser versions.
- **CSV**: Stores the scraped data in a structured format for analysis.
- **Logging**: Integrated logging system to track the scraping progress, handle errors, and log warnings.

## Detailed Workflow

1. **Setup Driver**: Initializes the Chrome WebDriver using WebDriver Manager, setting up implicit waits for page load times.
2. **Dynamic Scrolling**: Implements an automatic scrolling function to load all content on a page before extraction.
3. **Pagination**: Generates URLs for paginated vehicle listings, ensuring the scraper processes multiple pages of data.
4. **Data Extraction**: Extracts details from each vehicle card using Selenium’s element-finding capabilities:
   - **Title**: Identified by class name `vehicle-card-title`.
   - **Mileage**: Extracted from `vehicle-card-highlight`.
   - **Price**: Fetched from `price-value`.
   - **URL**: Captured through anchor tags to provide direct access to the listing.
5. **CSV Export**: Compiles the extracted data and saves it into a CSV file, ready for analysis.

## Example Usage

```python
from Honda_Crawler import scrape_multiple_sites_to_csv

# Define model filter and output file
model_filter = "Civic"
output_file = "vehicle_data.csv"

# Call function to scrape data and save to CSV
scrape_multiple_sites_to_csv(output_file, model_filter)
