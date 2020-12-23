FROM python:3.8.7-alpine
WORKDIR /jonasa_cloud
ADD . /jonasa_cloud
RUN apk update 
RUN apk add linux-headers gcc libc-dev g++ python3-dev
RUN pip3 install -r requirements.txt
CMD ["python","main.py"]
