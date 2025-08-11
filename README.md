🩺 CureSync – Digital Healthcare Platform
CureSync is a digital healthcare platform built with Django, HTML, CSS, and JavaScript, where patients can book doctor appointments and access various medical facilities online.

🚀 Features
🗓 Book appointments with doctors

📅 Manage and view appointments

💬 Contact healthcare providers

🔒 User authentication (Login & Signup)

📱 Responsive design

🛠 How to Run Locally
1️⃣ Clone the repository
git clone https://github.com/Piyash1/CureSync-digital_healthcare_platform.git
cd CureSync-digital_healthcare_platform

2️⃣ Create a virtual environment and activate it
python -m venv venv
# Activate virtual environment
venv\Scripts\activate     # Windows
source venv/bin/activate  # Mac/Linux

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Apply migrations
python manage.py migrate

5️⃣ Create a superuser (for admin access)
python manage.py createsuperuser

6️⃣ Run the development server
python manage.py runserver
The app will be available at: http://127.0.0.1:8000/

📦 Tech Stack
Backend: Django

Frontend: HTML, CSS, JavaScript

Database: SQLite (default)

📜 License
This project is licensed under the MIT License.
