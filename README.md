# CORS-Aware Metrics API

## Deploy on Render
1. Create a GitHub repository and upload `main.py`, `requirements.txt`, and `render.yaml`.
2. In Render, choose **New + → Blueprint** and connect that repository, or create a Web Service with:
   - Build command: `pip install -r requirements.txt`
   - Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
3. Wait for deployment and copy the public service URL.
4. Test `https://YOUR-SERVICE.onrender.com/stats?values=1,2,3,4`.
5. Submit only the base URL as the assignment answer.

## Local test
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Allowed origin: `https://dash-n1d87a.example.com`
Email: `24f1002110@ds.study.iitm.ac.in`
