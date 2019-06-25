FROM ubuntu:latest
COPY . /app
WORKDIR /app

RUN apt-get update
RUN apt-get install -y python3-pip python3-dev build-essential
RUN pip3 install -r requirements.txt

EXPOSE 8005
CMD ["python3", "main.py"]
