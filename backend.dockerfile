FROM python:3.9

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY . /app/

RUN chmod +x /app/prestart.sh

CMD ["/app/prestart"]

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
