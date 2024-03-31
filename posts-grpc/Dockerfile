FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /app
RUN mkdir /protos
WORKDIR /app

ADD ./posts-grpc/ /app/
ADD ./posts-grpc/requirements.txt requirements.txt
ADD ./protos/ /protos/

RUN apt update -y
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN python -m grpc_tools.protoc -I/protos --python_out=/app --pyi_out=/app --grpc_python_out=/app /protos/posts.proto

ENTRYPOINT ["python", "main.py"]