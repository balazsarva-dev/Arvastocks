# Arvastocks

Arvastocks is a stock management and analysis application built with a Flask backend and a React frontend. This guide will help you set up the project locally.

---

## Prerequisites

Before you begin, ensure you have the following installed:

1. **Docker Desktop**  
   - Download and install Docker Desktop: [Docker Desktop](https://www.docker.com/products/docker-desktop/)

2. **Node.js and npm**  
   - Download and install Node.js (npm comes bundled): [Node.js](https://nodejs.org/)

3. **Python**  
   - Ensure Python 3.10+ is installed on your system.

---

## Setup Instructions

### 1. Clone the Repository
```bash
cd <root-directory>
git clone https://github.com/LiZoMark841619/Arvastocks.git
cd Arvastocks
```

### 2. Set Up the Backend
1. Create a Python virtual environment:
   ```bash
   python -m venv venv
   ```
2. Activate the virtual environment:
   - **Windows**:
     ```bash
     source venv/Scripts/activate
     ```
   - **Mac/Linux**:
     ```bash
     source venv/bin/activate
     ```
3. Navigate to the `backend` directory:
   ```bash
   cd backend
   ```
4. Install the required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   - This process may take **5–10 minutes**.

5. Create an `.env` file in the `backend` directory with the following variables:
   ```env
   DB_HOST=stock_db
   DB_USER=root
   DB_PASSWORD=yourpassword
   DB_NAME=arvastocks
   API_KEY=your_api_key
   ```

### 3. Set Up the Frontend
1. Navigate to the `frontend` directory:
   ```bash
   cd ../frontend
   ```
2. Install the required Node.js dependencies:
   ```bash
   npm install
   ```

---

## Running the Application

1. Navigate back to the project root directory:
   ```bash
   cd ..
   ```
2. Start the application using Docker Compose:
   ```bash
   docker-compose up --build -d
   ```
3. Open your browser and navigate to:
   - **Frontend**: [http://localhost:5173](http://localhost:5173)  
     (React frontend server running locally)

---

## Notes
- Ensure Docker Desktop is running before executing `docker-compose up`.
- The backend API will be available at [http://localhost:5000/api](http://localhost:5000/api).
- If you encounter any issues, check the logs for the backend and frontend containers:
  ```bash
  docker logs stock_backend
  docker logs stock_frontend
  ```

---
