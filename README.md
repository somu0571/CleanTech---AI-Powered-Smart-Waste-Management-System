#🌿  CleanTech AI – Smart Waste Management System

An AI-powered waste management platform designed to make cities cleaner, smarter, and more sustainable. CleanTech AI enables citizens, admins, and recyclers to collaborate efficiently through intelligent waste classification, reporting, analytics, and eco-reward systems.

🚀 Features
👤 Citizen Module
🔬 AI-based waste classification (image upload)
♻️ Recycling guidance
📣 Report issues (illegal dumping, etc.)
🌱 Eco-points reward system
🏆 Leaderboard for engagement
🧑‍💼 Admin Module
📊 Dashboard with KPIs
🗺️ Waste heatmaps
📈 Predictive analytics
🚛 Route optimization
📋 Complaint management system
♻️ Recycler Module
📦 Manage collected waste
📥 View pickup requests
📊 Track recycling activities
🧠 Tech Stack
Frontend
Streamlit
Plotly (visualizations)
Custom CSS (premium UI)
Backend
FastAPI
JWT Authentication
REST APIs
AI / ML
Waste classification model (image-based)
Database
SQLite / PostgreSQL (configurable)
📂 Project Structure
CleanTech-AI/
│
├── backend/
│   ├── main.py
│   ├── routes/
│   ├── models/
│   └── utils/
│
├── frontend/
│   └── app.py
│
├── assets/
│
├── requirements.txt
└── README.md
⚙️ Installation & Setup
1️⃣ Clone the Repository
git clone https://github.com/somu0571/CleanTech---AI-Powered-Smart-Waste-Management-System.git
cd CleanTech---AI-Powered-Smart-Waste-Management-System
2️⃣ Backend Setup (FastAPI)
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

Backend runs at:

http://localhost:8000
3️⃣ Frontend Setup (Streamlit)
cd frontend
streamlit run app.py
🔐 Authentication

The system supports:

Citizen login
Admin login (with verification)
Recycler login (with verification)

JWT tokens are used for secure API communication.

🎨 UI Highlights
🌿 Modern green-themed UI
📊 Interactive dashboards
📱 Responsive layout
✨ Smooth animations & custom components
🧪 Future Enhancements
📍 Real-time GPS tracking for waste collection
🤖 Advanced AI classification models
🌐 Multi-language support
📲 Mobile app version
🔔 Push notifications
🤝 Contributing

Contributions are welcome!

Fork the repo
Create a new branch
Commit your changes
Submit a Pull Request
📜 License

This project is licensed under the MIT License.

💡 Inspiration

Built to promote sustainability and smarter urban living through AI-driven waste management.
