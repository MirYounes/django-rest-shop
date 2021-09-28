FROM python:3.9

WORKDIR /app

COPY requirements.txt /app/

RUN pip install -U pip
RUN pip install -r requirements.txt

COPY . /app/

EXPOSE 8000

CMD ["gunicorn","core.wsgi:application",":8000"]