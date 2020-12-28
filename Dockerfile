FROM python:3.8-slim
WORKDIR /jonasa_cloud
ADD . /jonasa_cloud
RUN apt-get update
RUN apt-get install python3-dev -y
RUN pip3 install -r requirements.txt
CMD ["python","main.py"]