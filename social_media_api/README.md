# Social Media API
A Django DRF backend for a social networking platform featuring JWT auth, user profiles, and followers system.

### 🛠 Tech Stack
- **Framework:** Django 6.0.2
- **API:** Django REST Framework
- **Auth:** SimpleJWT
- **Database:** PostgreSQL (or SQLite for local dev)
- **Image Processing:** Pillow 12.1.1

### User registraion and Authentication
#### Register new user:
send a POST requst to enpoint : 'accounts/register'
body: {
  "username": "your_name",
  "password": "your_password",
  "email": "email@example.com",
  "bio": "Hello world!"
}

#### Login existing account:
send POST request to endpoint: 'accounts/login'
body: {
  "username": "your_name",
  "password": "your_password",
}


