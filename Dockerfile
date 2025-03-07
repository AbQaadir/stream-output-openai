FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN groupadd -g 10016 choreo && \
    useradd --uid 10016 --gid 10016 --no-create-home --shell /bin/bash choreouser

USER 10016

EXPOSE 8080

CMD ["python", "main.py"]