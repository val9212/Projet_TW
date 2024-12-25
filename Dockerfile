FROM python:3.11.6
LABEL authors="val92"

WORKDIR /app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . /app

EXPOSE 8000

CMD ["python", "./myproject/manage.py", "runserver"]

