FROM python:3.10.0

ENV PYTHONUNBUFFERED=1
WORKDIR /usr/app/
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE ${PORT}
CMD ["bash", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:$PORT"]