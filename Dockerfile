FROM python:3.8
#install python 3.8

COPY . .
#copy project from current directory

RUN pip3

EXPOSE 5000
#open up port 5000 on the docker container

CMD ["python3","test_server.py"]
#run test_server.py