FROM python:3.9

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "-u", "./main.py"]

# Or enter the name of your unique directory and parameter set