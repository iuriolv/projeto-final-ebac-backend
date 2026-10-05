FROM python:3.14-slim

WORKDIR /code

COPY pyproject.toml poetry.lock* ./

RUN pip install "poetry==2.4.1" && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root

COPY . .

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]