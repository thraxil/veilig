FROM jjanzic/docker-python3-opencv:latest
RUN pip install boto3
RUN mkdir -p /app
WORKDIR /app
COPY . /app/
