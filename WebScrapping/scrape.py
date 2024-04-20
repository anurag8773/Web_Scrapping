import requests
from bs4 import BeautifulSoup
import openpyxl
import gspread
from openpyxl import Workbook
from oauth2client.service_account import ServiceAccountCredentials

# Define the URL to scrape
url = "https://www.google.com/maps/place/Moti+Mahal+Restaurant/@28.6436744,77.2021401,14z/data=!4m10!1m2!2m1!1sresturent!3m6!1s0x390cfd2076d5d8a7:0xfc425590701a73a6!8m2!3d28.6464743!4d77.2401149!15sCgpyZXN0YXVyYW50WgwiCnJlc3RhdXJhbnSSARFpbmRpYW5fcmVzdGF1cmFudOABAA!16s%2Fg%2F11b6nvwh1v?entry=ttu"

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
