import os
import re
import csv
import time
import json
import warnings
from datetime import datetime
from typing import List, Dict, Optional
import requests
from bs4 import BeautifulSoup
import pandas as pd
from dateutil import parser as dateparser
import certifi
import urllib3

# 🔕 Disable SSL / Insecure warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
warnings.filterwarnings("ignore", message="SSL error*")

BASE_URL = "https://www.ibps.in/"
LISTING_URLS = [
    "https://www.ibps.in/important-notice/",
    "https://www.ibps.in/career/"
]



OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
OUT_CSV = os.path.join(OUT_DIR, "ibps_jobs.csv")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0 Safari/537.36"
}

# Known date patterns IBPS uses often, e.g. "06.11.2025", "06/11/2025", "06-11-2025"
DATE_PATTERNS = [
    r'(\d{1,2}[\./-]\d{1,2}[\./-]\d{2,4})',
    r'([A-Za-z]{3,9}\s+\d{1,2},\s*\d{4})'
]

def safe_get(url: str, allow_insecure=False) -> Optional[requests.Response]:
    """
    Requests with retries and SSL fallback (verify=False as last resort).
    """
    for attempt in range(3):
        try:
            resp = requests.get(url, headers=HEADERS, timeout=20, verify=certifi.where())
            resp.raise_for_status()
            return resp
        except requests.exceptions.SSLError as ssl_err:
            if allow_insecure:
                warnings.warn(f"SSL error on {url}, retrying with verify=False (attempt {attempt+1})")
                try:
                    resp = requests.get(url, headers=HEADERS, timeout=20, verify=False)
                    resp.raise_for_status()
                    return resp
                except Exception:
                    time.sleep(1.5)
            else:
                time.sleep(1.5)
        except Exception:
            time.sleep(1.5)
    return None

def absolutize(href: str) -> str:
    if not href:
        return ""
    if href.startswith("http://") or href.startswith("https://"):
        return href
    return requests.compat.urljoin(BASE_URL, href)

def extract_date(text: str) -> Optional[str]:
    if not text:
        return None
    for pat in DATE_PATTERNS:
        m = re.search(pat, text)
        if m:
            date_text = m.group(1)
            try:
                dt = dateparser.parse(date_text, dayfirst=True)
                return dt.strftime("%Y-%m-%d")
            except Exception:
                continue
    return None

def guess_location(text: str) -> Optional[str]:
    """
    IBPS often doesn't include a location; try to infer 'All India' if national.
    """
    if not text:
        return None
    text_low = text.lower()
    if any(k in text_low for k in ["india", "nation", "pan india", "all india", "across india"]):
        return "All India"
    if "mumbai" in text_low:
        return "Mumbai"
    if "delhi" in text_low:
        return "Delhi"
    # Fallback unknown
    return None

def parse_listing_page(html: str) -> List[Dict]:
    soup = BeautifulSoup(html, "html.parser")
    items = []

    # Common areas on IBPS: lists of notices, post blocks, etc.
    candidates = []
    candidates += soup.select("ul li a")
    candidates += soup.select("article a")
    candidates += soup.select("div a")

    seen = set()
    for a in candidates:
        href = a.get("href")
        text = " ".join(a.get_text(strip=True).split())
        if not href or not text:
            continue
        url = absolutize(href)
        if url in seen:
            continue
        seen.add(url)

        # Heuristics: include links referencing recruitment/CRP/notification/advertisement
        if not re.search(r"(recruit|career|notification|advert|important|crp|cwe|exam)", text.lower()):
            continue

        title = text
        date_in_text = extract_date(text)
        items.append({
            "title": title,
            "url": url,
            "date_from_text": date_in_text
        })

    return items

def enrich_from_detail(url: str) -> Dict:
    resp = safe_get(url, allow_insecure=True)
    if not resp:
        return {"post_date": None, "location": None, "final_url": url}

    soup = BeautifulSoup(resp.text, "html.parser")
    # Try to find date
    meta_date = None
    for sel in [
        "time[datetime]",
        "meta[property='article:published_time']",
        "meta[name='date']",
        "meta[name='pubdate']",
        ".entry-date",
        ".post-date",
        ".td-post-date",
        "time"
    ]:
        node = soup.select_one(sel)
        if node:
            content = node.get("datetime") or node.get("content") or node.get_text(strip=True)
            meta_date = extract_date(content) or meta_date

    # Fallback: any date-like text on page
    if not meta_date:
        text = soup.get_text(" ", strip=True)
        meta_date = extract_date(text)

    # Location guess from page text
    location = guess_location(soup.get_text(" ", strip=True))
    return {
        "post_date": meta_date,
        "location": location,
        "final_url": resp.url  # after redirects
    }

def dedupe(items: List[Dict]) -> List[Dict]:
    seen = set()
    out = []
    for it in items:
        key = (it["title"].lower(), it["url"])
        if key in seen:
            continue
        seen.add(key)
        out.append(it)
    return out

def scrape() -> pd.DataFrame:
    all_items: List[Dict] = []
    for url in LISTING_URLS:
        resp = safe_get(url, allow_insecure=True)
        if not resp:
            continue
        page_items = parse_listing_page(resp.text)
        all_items.extend(page_items)
        time.sleep(0.8)

    all_items = dedupe(all_items)

    rows = []
    for it in all_items:
        detail = enrich_from_detail(it["url"])
        post_date = detail.get("post_date") or it.get("date_from_text")
        location = detail.get("location") or "All India"
        rows.append({
            "Job Title": it["title"],
            "Location": location,
            "Post/Publish Date": post_date or "",
            "Link": detail.get("final_url") or it["url"]
        })
        time.sleep(0.5)

    df = pd.DataFrame(rows)
    # Basic cleaning
    if not df.empty:
        # Make date uniform where possible
        def norm(d):
            if not d:
                return ""
            try:
                return dateparser.parse(d).strftime("%Y-%m-%d")
            except Exception:
                return d
        df["Post/Publish Date"] = df["Post/Publish Date"].apply(norm)

        # Sort newest first
        if "Post/Publish Date" in df.columns:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                df["__dt"] = pd.to_datetime(df["Post/Publish Date"], errors="coerce")
                df = df.sort_values("__dt", ascending=False).drop(columns="__dt")

    return df

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    df = scrape()
    if df.empty:
        print("No items found. (IBPS site may have changed or blocked scraping.)")
        # Write empty CSV with headers to still satisfy submission
        df = pd.DataFrame(columns=["Job Title", "Location", "Post/Publish Date", "Link"])

    df.to_csv(OUT_CSV, index=False, encoding="utf-8")
    print(f"Wrote {len(df)} rows to {OUT_CSV}")

if __name__ == "__main__":
    main()

