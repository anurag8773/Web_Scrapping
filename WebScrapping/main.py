import requests
from bs4 import BeautifulSoup
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Define the URL to scrape
url = "https://www.google.com/maps"

# Define categories of local businesses you want to scrape
categories = ["restaurants", "hotels", "gyms", "salons", "pet stores"]

# Google Sheet credentials
scope = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

print("Loading credentials...")
creds = ServiceAccountCredentials.from_json_keyfile_name('local-business-details-417521-871cae6abf80.json', scope)
print("Credentials loaded:", creds)

# Authenticate with Google Sheets API
client = gspread.authorize(creds)

# Open Google Sheet by providing the Google Sheet ID
sheet = client.open_by_key("14c4k5MN11tbClah15ve6zr_XGCvIFn4sS3Ag1VKG17M").sheet1


# Function to scrape business details
def scrape_business_details(category):
    response = requests.get(f"{url}/search/{category}")
    soup = BeautifulSoup(response.content, 'html.parser')
    
    businesses = soup.find_all("div", class_="section-result-content")
    
    for business in businesses:
        name = business.find("h3", class_="section-result-title").text.strip()
        address = business.find("span", class_="section-result-location").text.strip()
        phone = business.find("span", class_="section-result-phone-number")
        phone = phone.text.strip() if phone else ""
        website = business.find("a", class_="section-result-action")
        website = website['href'] if website else ""
        
        # Insert data into Google Sheet
        sheet.append_row([name, address, phone, website])

# Loop through categories and scrape business details
for category in categories:
    try:
        scrape_business_details(category)
        print(f"Scraped data for category '{category}' successfully.")
    except Exception as e:
        print(f"Error scraping data for category '{category}': {e}")

