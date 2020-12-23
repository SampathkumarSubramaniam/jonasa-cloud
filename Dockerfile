FROM python:3.8.7-alpine
WORKDIR /jonasa_cloud
ADD . /jonasa_cloud
RUN pip install -r requirements.txt
CMD ["python","main.py"]
