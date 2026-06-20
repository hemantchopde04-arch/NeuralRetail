FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install --default-timeout=300 pandas streamlit fastapi uvicorn

EXPOSE 8501
EXPOSE 8000

CMD ["streamlit", "run", "dashboard.py", "--server.address=0.0.0.0"]