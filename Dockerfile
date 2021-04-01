FROM python:3.7-stretch
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
ENV PORT 8080
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app
