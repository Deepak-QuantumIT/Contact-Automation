FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    firefox-esr \
    wget \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

ENV GECKODRIVER_VERSION v0.35.0
RUN wget -q "https://github.com/mozilla/geckodriver/releases/download/${GECKODRIVER_VERSION}/geckodriver-${GECKODRIVER_VERSION}-linux64.tar.gz" \
    && mkdir -p /app/drivers \
    && tar -xzf geckodriver-${GECKODRIVER_VERSION}-linux64.tar.gz -C /app/drivers \
    && rm geckodriver-${GECKODRIVER_VERSION}-linux64.tar.gz

ENV PATH="/app/drivers:${PATH}"

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

ENV FLASK_APP=app.py
ENV PYTHONUNBUFFERED=1

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
