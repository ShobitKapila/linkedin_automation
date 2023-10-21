import requests
from bs4 import BeautifulSoup
import pandas as pd

# Define your LinkedIn email and password
linkedin_email = "kapilashobit4@gmail.com"
linkedin_password = "Shobit@1234"

# Define the LinkedIn profile URL to scrape (e.g., your own profile)
linkedin_url = "https://www.linkedin.com/in/gurpreet%2Dsingh%2Dbawa%2D57ba9522b/"

# Set up a session for making requests with a logged-in LinkedIn account
session = requests.Session()
login_url = "https://www.linkedin.com/login"
response = session.get(login_url)
soup = BeautifulSoup(response.text, "html.parser")
csrf = soup.find("input", {"name": "loginCsrfParam"})["value"]

login_payload = {
    "session_key": linkedin_email,
    "session_password": linkedin_password,
    "loginCsrfParam": csrf,
}

session.post(login_url, data=login_payload)

# Now, you can scrape the LinkedIn profile page
profile_response = session.get(linkedin_url)
profile_soup = BeautifulSoup(profile_response.text, "html.parser")

# Customize the code to extract the data you need from the profile_soup
name_element = profile_soup.find("li", {"class": "inline t-24 t-black t-normal break-words"})
name = name_element.get_text() if name_element else "Name Not Found"

headline_element = profile_soup.find("h2", {"class": "mt1 t-18 t-black t-normal"})
headline = headline_element.get_text() if headline_element else "Headline Not Found"

# Extract experience, education, and projects
experience = []
education = []
projects = []

experience_section = profile_soup.find("section", {"id": "experience-section"})
if experience_section:
    for entry in experience_section.find_all("li", {"class": "pv-position-entity"}):
        experience.append(entry.get_text())

education_section = profile_soup.find("section", {"id": "education-section"})
if education_section:
    for entry in education_section.find_all("li", {"class": "pv-education-entity"}):
        education.append(entry.get_text())

projects_section = profile_soup.find("section", {"id": "projects-section"})
if projects_section:
    for entry in projects_section.find_all("li", {"class": "pv-profile-section__card-item"}):
        projects.append(entry.get_text())

# Create a DataFrame
data = {
    "Name": [name],
    "Headline": [headline],
    "Experience": [", ".join(experience)],
    "Education": [", ".join(education)],
    "Projects": [", ".join(projects)],
}

df = pd.DataFrame(data)

# Save to an Excel file
excel_file = "linkedin_profile.xlsx"
df.to_excel(excel_file, index=False, engine="openpyxl")
print(f"Data saved to {excel_file}")
