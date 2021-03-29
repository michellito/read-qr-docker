# set base image (host OS)
FROM python:3.8

# copy the dependencies file to the working directory
COPY requirements.txt .
COPY transfer.py .

# install dependencies
RUN pip install -r requirements.txt

ENTRYPOINT ["python3", "transfer.py"]