# IBPS Web Scraper + API

This project scrapes public **IBPS** recruitment/notice links and saves them to **CSV** (Pandas), then exposes a **Django REST API** to read the CSV.

- **Manual scraping** (per your requirement)
- **CSV fields**: Job Title, Location, Post/Publish Date, Link
- **Endpoints**: `GET /api/jobs/`, `GET /api/jobs/<id>/`
- **Postman collection** included

---

## Project Structure

scraper/
├─ data/ibps_jobs.csv # generated output
├─ scripts/scrape_ibps.py # standalone scraper (manual)
├─ src/core/ # Django project root
│ └─ jobs/ # API app
└─ postman/IBPS Jobs API.postman_collection.json


---

## 1) Setup

```bash
# From the parent directory where you want the project
cd scraper

# Create & activate virtual environment (Windows PowerShell)
python -m venv venv
venv\Scripts\activate

# Or on macOS/Linux:
# python3 -m venv venv
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

2) Run the Scraper (Manual)

Two equivalent options:

Option A: Standalone script
python scripts/scrape_ibps.py
# Output: data/ibps_jobs.csv

Option B: Django management command
python src/core/manage.py scrape_ibps
# Output: data/ibps_jobs.csv


If you face SSL errors with ibps.in, the scraper automatically retries and falls back to verify=False as a last resort.

3) Start the API
# (Initial migrations—no models here, but Django needs a DB file)
python src/core/manage.py migrate

# Run dev server
python src/core/manage.py runserver


Open:

List: http://127.0.0.1:8000/api/jobs/

Detail: http://127.0.0.1:8000/api/jobs/1/

Note: Re-run the scraper whenever you want fresh data; the API always reads from data/ibps_jobs.csv.

4) Postman Collection

Import postman/IBPS Jobs API.postman_collection.json into Postman.

Set base_url variable to:

http://127.0.0.1:8000


Use:

List Jobs → GET /api/jobs/

Job Detail → GET /api/jobs/<id>/

5) Git Commands (push existing repo)
# Initialize repo
git init
git add .
git commit -m "IBPS scraper + API + Postman"

# Create new GitHub repo named `scraper` (on GitHub UI), then:
git branch -M main
git remote add origin https://github.com/<your-username>/scraper.git
git push -u origin main

6) Notes / Troubleshooting

0 results? IBPS may change markup. The scraper uses robust heuristics across:

/, /career/, and /important-notice/ pages

Filters for links mentioning recruit, career, notification, advert, CRP, etc.

Dates are parsed from visible text and page metadata when available.

Location is often not published; defaults to All India unless inferred.

SSL errors: We use certifi and, if needed, retry with verify=False.

7) Submission Checklist

✅ Repo link shared (push the folder to GitHub and share)

✅ Postman collection provided (postman/IBPS Jobs API.postman_collection.json)


---

# Terminal Commands (all together)

```bash
# 0) Go to where you want to place the project folder
# (You already have the folder named 'scraper' as requested.)

# 1) Create venv & install deps
cd scraper
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# 2) Run scraper (manual)
python scripts/scrape_ibps.py

# 3) Start API
python src/core/manage.py migrate
python src/core/manage.py runserver

# 4) Test
# http://127.0.0.1:8000/api/jobs/
# http://127.0.0.1:8000/api/jobs/1/

# 5) GitHub push
git init
git add .
git commit -m "IBPS scraper + API + Postman"
git branch -M main
git remote add origin https://github.com/ANSHAD-AHAMMED/Pinak-Venture-Task.git
git push -u origin main