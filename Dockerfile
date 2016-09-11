FROM python:2-slim

MAINTAINER John Harris <john@johnharris.io>

EXPOSE 5000

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

ENTRYPOINT ["python"]

CMD ["engine.py"]
