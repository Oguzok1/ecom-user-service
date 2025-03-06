FROM python:3.12-alpine


ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

RUN pip install poetry \
    && poetry config virtualenvs.create false

WORKDIR /app

COPY . .

RUN poetry install --no-interaction --no-ansi

EXPOSE 8001

CMD ["poetry", "run", "python", "-m", "ecom_user_service.app"]