FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y wget curl gnupg ca-certificates &&     curl -fsSL https://dl.google.com/linux/linux_signing_key.pub |     gpg --dearmor -o /usr/share/keyrings/google-chrome.gpg &&     echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main"     > /etc/apt/sources.list.d/google-chrome.list &&     apt-get update && apt-get install -y google-chrome-stable &&     rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN mkdir -p uploads output

EXPOSE 7860

CMD ["python", "app.py"]
