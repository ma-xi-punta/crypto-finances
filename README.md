# Crypto Finances - Cryptocurrency Portfolio

Crypto Finances is a comprehensive application that allows users to track their cryptocurrency portfolio in real-time. It uses FastAPI for the backend and Streamlit for the graphical interface, providing a fast and intuitive experience.

---

## Main Features
FastAPI API to manage transactions and query portfolio data.
Interactive interface with Streamlit, optimized for usability and visualization.
Dynamic charts to visualize the portfolio distribution.
Real-time connection with cryptocurrency data.
Modular design with a scalable architecture. 

---

## Technologies Used
Python 3.10+
FastAPI (for the backend)
Uvicorn (to run the server)
Streamlit (for the visual interface)
Matplotlib & Pandas (for charts and data manipulation)
Requests (for API integration)

---

##  Installation and Execution

### 1️⃣ Clone the repository
```bash
git clone https://github.com/tu-usuario/crypto-finances.git
cd crypto-finances
```

### 2️⃣ Create a virtual environment and install dependencies
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r backend/requirements.txt
pip install streamlit matplotlib pandas requests
```

### 3️⃣ Start the backend (API with FastAPI)
```bash
uvicorn backend.main:app --reload
```
🔹 Access the API documentation at: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### 4️⃣ Start the frontend (Interface with Streamlit)
```bash
streamlit run app.py
```
🔹 The application will open in your browser at:  [http://localhost:8501](http://localhost:8501)

---

## 📸 Screenshots

### **Portfolio Visualization**
[Portfolio Screenshot](images/captura_portafolio.png)

---

##  Main API Endpoints

| GET | `/api/transactions/` |  Get all registered transactions |
| POST | `/api/transactions/` | Add a new transaction |
| GET | `/api/portfolio/` | Query the current portfolio status |

---

## 📩 Contact
📧  If you're interested in this project or want to collaborate, feel free to contact me at [maxisimonelli147@mail.com]!

📌 ** LinkedIn Profile**: [https://www.linkedin.com/in/maximiliano-simonelli-288794203/]

📌 **PGitHub Portfolio**: [https://github.com/ma-xi-punta]



