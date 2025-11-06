IBPS Login API (Django REST Framework + JWT)

A simple Django REST API project that provides a login authentication system using JWT (JSON Web Token) with a basic HTML UI login page.

✅ Features

/api/login/ accepts username & password

Valid credentials return a JWT access token

Invalid credentials return an error

Test user is automatically created:

username: testuser
password: testpass


Includes a simple UI (/) to test login without Postman

Uses SQLite database

📂 Project Structure
ibps_api/
├── manage.py
├── requirements.txt
├── README.md
├── ibps_api/
│   ├── settings.py
│   ├── urls.py
├── accounts/
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── signals.py
└── templates/
    └── login.html

🧠 Tech Stack
Component	Technology
Backend	Django + Django REST Framework
Authentication	JWT (SimpleJWT)
Database	SQLite
UI	Pure HTML + JavaScript (Fetch API)
▶️ How to Run
1. Create and activate virtual environment
python -m venv venv


Windows:

venv\Scripts\activate


macOS / Linux:

source venv/bin/activate

2. Install dependencies
pip install -r requirements.txt

3. Apply migrations
python manage.py migrate

4. Run server
python manage.py runserver

🧪 Testing the API
✅ Via Postman / Thunder Client

POST

http://127.0.0.1:8000/api/login/


Body (JSON):

{
  "username": "testuser",
  "password": "testpass"
}


If valid, response:

{
  "token": "<jwt_access_token>"
}


If invalid:

{
  "error": "Invalid credentials"
}

🖥 Testing UI (Login Form)

Open browser and go to:

http://127.0.0.1:8000/


Enter:

username: testuser
password: testpass


You will see:

✅ Token: eyJhbGciOiJIUzI...

🔧 Endpoints
Method	URL	Purpose
POST	/api/login/	Authenticate user and return JWT token
GET	/	Displays simple login UI (HTML form)
📌 Notes

JWT token must be sent in headers when calling authenticated API:

Authorization: Bearer <token>


This project is for learning and demonstration purposes.

✨ Author

Developed as per Django REST Framework task requirement.