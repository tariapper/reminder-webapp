FROM python:3.8
#install python 3.8

COPY .. .
#copy project from current directory

COPY app/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
#RUN pip3 install bottle
#RUN pip3 install flask

EXPOSE 5000
#open up port 5000 on the docker container

#CMD ["python3","test_server.py"]
#CMD ["python3","bottle_server.py"]
CMD ["python3","flask_server.py"]
#run test_server.py