# Stock Market Analyst AI

## Setup Instructions

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Generate API Keys:
   Copy `.env.example` to `.env` and fill the variables.

3. Run the backend:
   ```bash
   uvicorn backend.main:app --reload
   ```

4. Run the frontend:
   ```bash
   streamlit run frontend/streamlit_app.py
   ```
