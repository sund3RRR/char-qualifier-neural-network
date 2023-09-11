FROM python:3.11.5-bookworm

RUN set -eux; \
    apt-get update

WORKDIR /app

COPY ./app/char-qualifier-neural-network/ /app/

RUN set -eux; \
    pip install pip --upgrade; \
    pip install -r requirements.txt

EXPOSE 8080
# CMD ["ls", "-la"]
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]