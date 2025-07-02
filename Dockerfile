FROM python:3.10-slim

# Install system deps
RUN apt-get update && apt-get install -y wget gnupg unzip curl libglib2.0-0 libnss3 libgconf-2-4 libatk1.0-0 libatk-bridge2.0-0 libcups2 libxss1 libxcomposite1 libxrandr2 libasound2 libxtst6 libgtk-3-0 libxdamage1 libgbm1 && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright and its browser
RUN playwright install --with-deps

# Add app code
COPY app.py .

CMD ["gunicorn", "--bind", "0.0.0.0:10000", "app:app"]
