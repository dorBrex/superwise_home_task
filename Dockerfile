# syntax=docker/dockerfile:1

FROM python:3.8

WORKDIR /superwise_home_assignment

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

EXPOSE 8080/tcp

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]