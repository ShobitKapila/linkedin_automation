from linkedin_api import Linkedin
import getpass
import pandas as pd

# Replace with your LinkedIn app credentials
client_id = "YOUR_CLIENT_ID"
client_secret = "YOUR_CLIENT_SECRET"

username = input("Your LinkedIn username/email: ")
password = getpass.getpass("Your LinkedIn password: ")

api = Linkedin(client_id, client_secret)
api.login(username, password)
domain = "Specific Domain"  # Replace with the domain you're interested in
results = []

# Number of pages to scrape
pages_to_scrape = 5

for page in range(1, pages_to_scrape + 1):
    search_results = api.search_people(
        network_depth="S",
        keywords=f'"{domain}"',
        page=page
    )
    results.extend(search_results)

data = []

for result in results:
    # Customize the data you want to store in the Excel file
    name = result.get("name", "")
    title = result.get("headline", "")
    location = result.get("location", "")
    connections = result.get("numConnections", 0)
    data.append([name, title, location, connections])

# Create a DataFrame
df = pd.DataFrame(data, columns=["Name", "Title", "Location", "Connections"])

# Save to an Excel file
excel_file = "linkedin_profiles.xlsx"
df.to_excel(excel_file, index=False, engine="openpyxl")
print(f"Data saved to {excel_file}")
