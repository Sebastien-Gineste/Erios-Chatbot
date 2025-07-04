FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -u 1000 user

COPY --chown=user ./chatbot/ /app/
COPY --chown=user ./requirements.txt /app/requirements.txt

RUN pip3 install --no-cache-dir -r /app/requirements.txt

USER user

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "./chat.py", "--server.port=8501", "--server.address=0.0.0.0"]