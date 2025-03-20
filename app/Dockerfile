FROM python:3.11

ENV WORKDIR /app
ENV USER user

WORKDIR $WORKDIR

RUN apt-get update && \
    apt-get install -y netcat-traditional

RUN pip install --upgrade pip && \
    pip install --no-cache-dir poetry==1.7.1 && \
    poetry config virtualenvs.create false

COPY ../poetry.lock poetry.lock
COPY ../pyproject.toml pyproject.toml

RUN poetry install

COPY . .

ENV PYTHONPATH="${PYTHONPATH}:./app"

CMD ["sh", "-c", "uvicorn app.main:app --host ${FASTAPI_HOST} --port ${FASTAPI_PORT}"]
