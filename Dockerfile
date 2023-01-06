FROM python:3.10
WORKDIR /app
COPY . .

RUN chmod +x install.sh

EXPOSE 8080
ENV PYTHONUNBUFFERED True

RUN python -m pip install --upgrade pip
RUN pip install psycopg2-binary
RUN pip install flask-sqlalchemy
RUN pip install --no-cache-dir -r requirements.txt

CMD gunicorn -w 1 --bind=0.0.0.0:8080 'src:create_app()'