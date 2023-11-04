FROM python:3.11.4
WORKDIR /app


RUN apt-get update && apt-get install -y build-essential

RUN pip install --upgrade pip

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app
CMD ["daphne", "-b", "0.0.0.0:8000", "chattey.asgi:application"]