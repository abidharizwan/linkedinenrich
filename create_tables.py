# setup_database.py

import sqlite3

def setup_database():
    conn = sqlite3.connect("company_data.db")
    cursor = conn.cursor()

    # Create the linkedin_data table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS linkedin_data(
            cid INTEGER PRIMARY KEY,
            linkedin_url TEXT NOT NULL
        )
    """)

    # Insert data into linkedin_data
    data = [
        (68560774, "http://www.linkedin.com/company/insurance-commission-of-the-bahamas"),
        (18090, "http://www.linkedin.com/company/jefferson-county-public-schools"),
        (380979, "http://www.linkedin.com/company/fayette-county-public-schools-ky"),
        (95723504, "http://www.linkedin.com/company/everwise-cu"),
        (35096, "http://www.linkedin.com/company/peabody-trust"),
        (24593, "http://www.linkedin.com/company/wsfs-bank"),
        (166821, "http://www.linkedin.com/company/vitas-healthcare"),
        (8453, "http://www.linkedin.com/company/citgo"),
        (16156516, "http://www.linkedin.com/company/thecpso"),
    ]
    
    cursor.executemany("""
        INSERT OR IGNORE INTO linkedin_data (cid, linkedin_url)
        VALUES (?, ?)
    """, data)

    # Create the enriched_data table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS enriched_data (
            id INTEGER PRIMARY KEY,
            companyName TEXT,
            websiteUrl TEXT,
            hashtag TEXT,
            industry TEXT,
            description TEXT,
            followerCount INTEGER,
            employeeCount INTEGER,
            cid INTEGER,
            FOREIGN KEY (cid) REFERENCES linkedin_data (cid)
        )
    """)

    conn.commit()
    conn.close()

# Run the setup function
if __name__ == "__main__":
    setup_database()
