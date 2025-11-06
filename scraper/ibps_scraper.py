"""
ibps_scraper.py
----------------
A web scraper for fetching the latest recruitment/job notifications
from the official IBPS (Institute of Banking Personnel Selection) website.

Libraries Used:
- requests
- beautifulsoup4
- pandas

Output:
- A CSV file named 'ibps_jobs.csv' containing job title, location (if available),
  post date, and job link.

Run Command:
    python ibps_scraper.py
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import urllib3


urllib3.disable_warnings()  # suppress SSL warnings



# ----------------------------
# Function: Fetch HTML Content
# ----------------------------
def fetch_page(url):
    """Fetch the HTML content from the given URL with error handling."""
    try:
        response = requests.get(url, timeout=10, verify=False)  # 🔥 disable SSL verification
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None


# ----------------------------
# Function: Parse Job Listings
# ----------------------------
def parse_ibps_jobs(html):
    """
    Parse the IBPS career/recruitment page HTML
    and extract job listings with details.
    """
    soup = BeautifulSoup(html, "html.parser")
    job_data = []

    # The IBPS site lists notifications inside elements with class "latest-news" or similar.
    # We'll search for all <a> tags inside the latest updates section.
    updates_section = soup.find("div", class_="latest-news")

    if not updates_section:
        # Fallback: some pages use "post-content" or "widget_text"
        updates_section = soup.find("div", class_="post-content") or soup

    links = updates_section.find_all("a", href=True)

    for link in links:
        title = link.get_text(strip=True)
        if not title:
            continue

        href = link["href"]
        # Some links are relative, make them absolute
        if not href.startswith("http"):
            href = "https://www.ibps.in/" + href.lstrip("/")

        # Try to find date near the link text (if available)
        parent_text = link.find_parent().get_text(" ", strip=True)
        date_str = None
        for token in parent_text.split():
            if any(ch.isdigit() for ch in token) and "-" in token or "/" in token:
                date_str = token
                break

        # Location is rarely mentioned; leave empty or try to infer
        location = ""

        job_data.append({
            "Job Title": title,
            "Location": location,
            "Post/Publish Date": date_str if date_str else "",
            "Job Link": href
        })

    return job_data


# ----------------------------
# Function: Save to CSV
# ----------------------------
def save_to_csv(data, filename):
    """Save job data to a CSV file using pandas."""
    if not data:
        print("No data found to save.")
        return
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False, encoding="utf-8-sig")
    print("Data saved successfully")


# ----------------------------
# Main Script Execution
# ----------------------------
def main():
    base_url = "https://www.ibps.in"
    html = fetch_page(base_url)
    if not html:
        return

    jobs = parse_ibps_jobs(html)
    save_to_csv(jobs, "ibps_jobs.csv")


if __name__ == "__main__":
    main()
