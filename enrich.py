# fetch_and_populate_data.py

import os
import sqlite3
import dotenv
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
dotenv.load_dotenv()

# Constants
URL = os.getenv("API_ENDPOINT")
API_KEY = os.getenv("RAPID_API_KEY")

def fetch_and_populate_data():
    conn = sqlite3.connect("company_data.db")
    cursor = conn.cursor()

    # Read linkedin_urls from linkedin_data table
    cursor.execute("SELECT linkedin_url, cid FROM linkedin_data")
    rows = cursor.fetchall()

    # Create payload for API request
    payload = {"links": [row[0] for row in rows]}

    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": "linkedin-bulk-data-scraper.p.rapidapi.com",
        "Content-Type": "application/json",
    }

    # Make API request
    response = requests.post(URL, json=payload, headers=headers)
    json_data = response.json()
    print(json_data)

    if json_data.get("success") and json_data.get("status") == 200:
        for scrapped_data in json_data.get("data", []):
            company_data = scrapped_data.get("data", None)
            if not company_data:
                continue
    
            company_object = {
                "companyName": company_data.get("companyName", None),
                "companyId": company_data.get("companyId", None),
                "websiteUrl": company_data.get("websiteUrl", None),
                "hashtag": company_data.get("hashtag", None),
                "industry": company_data.get("industry", None),
                "description": company_data.get("description", None),
                "followerCount": company_data.get("followerCount", None),
                "employeeCount": company_data.get("employeeCount", None),
            }

            # Print the company object 
            print(company_object)

            # Insert data into enriched_data table
            cursor.execute("""
                INSERT INTO enriched_data (
                    companyName, websiteUrl, hashtag, industry, description,
                    followerCount, employeeCount,cid
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                company_object["companyName"],
                company_object["websiteUrl"],
                company_object["hashtag"],
                company_object["industry"],
                company_object["description"],
                company_object["followerCount"],
                company_object["employeeCount"],
                company_object["companyId"]
            ))
    
        
   

    conn.commit()
    conn.close()

# Run the fetch and populate function
if __name__ == "__main__":
    fetch_and_populate_data()
