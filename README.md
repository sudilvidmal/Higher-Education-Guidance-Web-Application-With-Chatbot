# 🎓 Higher Education Guidance Web Application with AI Chatbot

A smart web platform to help students explore higher education opportunities with the assistance of an AI-powered chatbot. The application enables secure login using LinkedIn API and provides personalized guidance based on user queries, preferences, and program availability.

---

## 🧰 Technologies Used

- **Frontend:** HTML5, CSS3, JavaScript, Bootstrap
- **Backend:** Python (Flask)
- **Database:** MySQL (via pyodbc)
- **AI/NLP:** Python + NLTK (Natural Language Toolkit)
- **Authentication:** LinkedIn OAuth 2.0 API
- **Cross-Origin Access:** Flask-CORS

---

## 🚀 Key Features

- 🤖 AI Chatbot built with Python NLP (NLTK) for real-time educational guidance
- 🔐 LinkedIn Login using OAuth 2.0 for secure authentication and profile validation
- 🎯 Program search by course, field, location, and qualification
- 🧑‍🎓 Student-friendly UI with responsive design
- 📊 Admin dashboard or interface for managing content *(if applicable)*
- 🧠 Real-time conversation flow with smart response generation

---

## 📦 Dependencies

Make sure you have **Python 3.7+** installed.

```bash
python3 -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate

# Install Required Libraries
pip install Flask
pip install nltk
pip install pyodbc
pip install flask-cors

# At the top of your nltk_utils.py or chatbot setup file, add:
import nltk
nltk.download('punkt')
