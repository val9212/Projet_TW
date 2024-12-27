FROM python:3.11.6
LABEL authors="val92"

WORKDIR /app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . /app

WORKDIR /app/myproject

CMD ["python", "./manage.py", "runserver", "0.0.0.0:8000"]

