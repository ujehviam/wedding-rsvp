# Wedding RSVP App

A simple web-based Wedding RSVP application that allows invited guests to confirm their attendance by submitting their **name**, **email address**, and **relationship to the couple**.

This project is intentionally minimal and practical, designed to demonstrate basic full‑stack concepts such as form handling, database integration, and containerized deployment.

---

## ✨ Features

* RSVP form for wedding guests
* Collects:

  * Guest name
  * Email address
  * Relationship to the couple
* Stores submissions in a PostgreSQL database
* Dockerized setup for easy local development
* Ready for CI/CD via GitHub Actions

---

## 🛠️ Tech Stack

* **Backend:** Python (Flask)
* **Database:** PostgreSQL
* **ORM:** SQLAlchemy
* **Containerization:** Docker
* **CI/CD:** GitHub Actions

---

## 🚀 Getting Started

### Prerequisites

* Docker
* Docker Compose
* Git

---

### Clone the Repository

```bash
git clone https://github.com/ujehviam/wedding-rsvp.git
cd wedding-rsvp
```

---

### Run the Application

```bash
docker compose up --build
```

The application will be available at:

```
http://localhost:5000
```

---

## 📂 Project Structure

```
Wedding-RSVP/
├── app/
│   ├── main.py
│   ├── models.py
│   └── templates/
├── .github/workflows/
│   └── ci.yml
├── docker-compose.yml
├── Dockerfile
└── README.md
```

---

## 🧪 CI/CD

This repository includes a **GitHub Actions workflow** that automatically runs on pushes and pull requests to ensure the application builds successfully.

---

## 📌 Future Improvements

* RSVP status (attending / not attending)
* Admin dashboard to view responses
* Email confirmation for guests
* Input validation and spam protection

---

## 📄 License

This project is for educational and personal use.

---

## 🙌 Acknowledgements

Built as a learning project to strengthen Docker, CI/CD, and backend development skills.
