FROM python:3.8

WORKDIR /app

RUN pip install pandas

COPY . .

CMD ["python", "./solution/main.py"]