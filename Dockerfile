FROM python:3.8.16-slim as base

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Disable check pip version
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

ENV PATH="/venv/bin:$PATH"
ENV PYTHONPATH "${PYTHONPATH}:/taz"


# --- build image ----
FROM base as builder

# extra repository
ARG PIP_EXTRA_INDEX_URL

ADD requirements/ ./requirements
ADD requirements.txt .

RUN python -m venv /venv && \
    apt update && apt install -y build-essential && \
    python -m pip install --no-cache-dir -r requirements.txt


# --- Release image ----
FROM base AS release
WORKDIR /app
COPY --from=builder /venv /venv
ADD . /app
