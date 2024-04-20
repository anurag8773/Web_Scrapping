import requests
from bs4 import BeautifulSoup
import openpyxl
import gspread
from openpyxl import Workbook
from oauth2client.service_account import ServiceAccountCredentials

# Define the URL to scrape
url = ""

# Define categories of local businesses you want to scrape
categories = ["restaurants", "hotels", "gyms", "salons", "pet stores"]

# Google Sheet credentials
scope = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

print("Loading credentials...")
creds = ServiceAccountCredentials.from_json_keyfile_name('*', scope)
print("Credentials loaded:", creds)

# Authenticate with Google Sheets API
client = gspread.authorize(creds)

# Open Google Sheet by providing the Google Sheet ID
sheet = client.open_by_key("*").sheet1

# Create a new Excel workbook and select the active sheet
wb = Workbook()
ws = wb.active

# Write headers to the Excel sheet
ws.append(["Name", "Address", "Phone", "Website"])

# Function to scrape business details
def scrape_business_details(category):
    response = requests.get(f"{url}/search/{category}")
    print("Request status code:", response.status_code)  # Debug: Print status code
    soup = BeautifulSoup(response.content, 'html.parser')
    
    businesses = soup.find_all("div", class_="section-result-content")
    print("Number of businesses found:", len(businesses))  # Debug: Print number of businesses found
    
    for business in businesses:
        name = business.find("h3", class_="section-result-title").text.strip()
        address = business.find("span", class_="section-result-location").text.strip()
        phone = business.find("span", class_="section-result-phone-number")
        phone = phone.text.strip() if phone else ""
        website = business.find("a", class_="section-result-action")
        website = website['href'] if website else ""
        
        # Insert data into Google Sheet
        sheet.append_row([name, address, phone, website])
        
        # Write data to Excel sheet
        ws.append([name, address, phone, website])
        print("Added data to Google Sheet and Excel:", [name, address, phone, website])  # Debug: Print added data

# Loop through categories and scrape business details
for category in categories:
    try:
        scrape_business_details(category)
        print(f"Scraped data for category '{category}' successfully.")
    except Exception as e:
        print(f"Error scraping data for category '{category}': {e}")

# Save the workbook to a file
wb.save("local_business_details.xlsx")

print("Data written to Excel sheet successfully.")
