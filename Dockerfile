# syntax=docker/dockerfile:1

FROM python:3.12.2

RUN mkdir /code

WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "src.app.main:app", "--host=0.0.0.0", "--port=3100"]
