from python:3.9


WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 8080

ENTRYPOINT ["python"]
CMD ["app.py", "-ac", "config.json", "run"]