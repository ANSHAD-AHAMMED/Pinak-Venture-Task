
# 🚀 Pinak Venture – Demo Task Submission  
Python / Django Developer Assignment

---

## ✅ Overview

This repository contains the solution for the demo assignment given by **Pinak Venture** for the role of **Python / Django Developer**.

The assignment consists of **two tasks**:

1. Web Scraping (IBPS Job Listings)
2. Django REST API (Login endpoint with Token Authentication)

---

---

# 🧩 Task 1 — Web Scraping (IBPS Jobs)

### 📌 Objective

Scrape job listings from the **IBPS official recruitment/career page** and extract:

| Field | Description |
|--------|-------------|
| Job Title | Name of the job post |
| Location | Job location (if available) |
| Publish Date | Date when job was posted |
| Link | URL to detailed job page |

---

### 📁 Files Included

```

scraper/
│── ibps_scraper.py          # Main script
│── ibps_jobs.csv            # Output CSV generated after running script
└── requirements.txt

```

---

### ▶️ How to Run (Web Scraper)

1. Open terminal and navigate into scraper folder:
```

cd scraper

```

2. Install dependencies:
```

pip install -r requirements.txt

```

3. Run the script:
```

python ibps_scraper.py

```

✅ `ibps_jobs.csv` will be generated automatically after execution.

---

---

# ⚙️ Task 2 — Django REST API (Login Authentication)

### 📌 Objective

Create a Django REST API with a login endpoint:

```

POST /api/login/

```

### ✅ Requirements Achieved

- Accepts JSON body with username and password
- Validates Django user credentials
- Returns authentication token (JWT or Auth Token)
- Auto-creates a test user:

```

Username: testuser
Password: testpass

```

---

### 📁 Project Structure

```

api/
│── manage.py
│── requirements.txt
│
├── ibps_api/
│   ├── settings.py
│   ├── urls.py
│
└── accounts/
├── views.py
├── serializers.py
├── urls.py

```

---

### ▶️ How to Run (Django API)

1. Open terminal:
```

cd api

```

2. Install dependencies:
```

pip install -r requirements.txt

```

3. Apply migrations:
```

python manage.py migrate

```

4. Run server:
```

python manage.py runserver

```

---

### 📬 Testing the Login API (Postman / Thunder Client)

**Endpoint:**
```

POST [http://127.0.0.1:8000/api/login/](http://127.0.0.1:8000/api/login/)

````

**Body (JSON):**
```json
{
  "username": "testuser",
  "password": "testpass"
}
````

**Response (Success):**

```json
{
  "token": "<generated_token>"
}
```

**Response (Failed):**

```json
{
  "error": "Invalid credentials"
}
```

---

### 📁 Postman Collection

A Postman collection is included in:

```
postman/IBPS_API_Postman_Collection.json
```

Import it into Postman → Hit Send → You will receive authentication token.

---

---

# ✅ Submission Confirmation Format

**This message must be sent to the company after pushing the repo:**

```
I confirm I have read the complete job posting (including salary and terms), and I accept the demo task. The repository link is <repo_link>. I will submit by Friday (07-11-2025).
```

---

---

# 🧪 Final Checklist

| Requirement              | Status      |
| ------------------------ | ----------- |
| IBPS Web Scraping Script | ✅ Completed |
| CSV Export               | ✅ Generated |
| Django REST API Login    | ✅ Working   |
| Token Authentication     | ✅ Returned  |
| Postman Collection       | ✅ Exported  |
| Repo Ready to Submit     | ✅ All Set   |

---

## 👨‍💻 Developer

**Name:** Anshad Ahammed
**Role:** Python / Django Developer
**Tools Used:** Python, Django, Django REST Framework, Pandas, BeautifulSoup

---

### 📄 License

This project is for evaluation/demo purposes only and should not be used commercially.

---

```

---

If you need:

- `requirements.txt`
- `.gitignore`
- final GitHub commit message

Just tell me **"Generate requirements + gitignore"** and I’ll generate them.
```
