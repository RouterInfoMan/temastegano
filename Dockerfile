FROM python:3.9

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
COPY . .

EXPOSE 80
# Set the entry point to run the Flask app
ENTRYPOINT ["python", "web_server.py"]