FROM python:3.10.0-alpine

RUN apk update && apk add gcc musl-dev

WORKDIR /usr/app/

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["sh", "-c",  "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
