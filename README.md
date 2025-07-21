# HROne Backend (BASE URL: https://hrone-backend-f4n8.onrender.com)

This is a FastAPI backend service for managing products and orders, connected to MongoDB.


## Project Structure

```
HRoneBackend/
│
├── main.py              # FastAPI app entrypoint
├── routes/              # API route modules
│   ├── products.py
│   └── orders.py
├── db.py                # MongoDB connection logic
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (ignored in git)
├── .gitignore           # Files/folders to ignore in git
```

## Setup & Run Locally

1. **Clone the repository:**
   ```powershell
   git clone https://github.com/Deepak-kumar4/HRone-Backend
   cd HRoneBackend
   ```

2. **Create and activate a virtual environment:**
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

4. **Set up your `.env` file:**
   ```
   MONGO_URL=<your-mongodb-connection-string>
   ```

5. **Run the server:**
   ```powershell
   python -m uvicorn main:app --reload
   ```
   The API will be available at [http://localhost:8000](http://localhost:8000).

## Deployment (Render)

1. Push your code to GitHub.
2. Ensure `render.yaml` is present in the project root.
3. Create a new Web Service on [Render](https://render.com/) and connect your repo.
4. Render will use `render.yaml` to build and run your app.

## API Endpoints
Base URL: https://hrone-backend-f4n8.onrender.com

