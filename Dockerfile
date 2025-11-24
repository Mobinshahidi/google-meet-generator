FROM python:3.11-slim
WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY src ./src
COPY .env.example ./

ENV PORT=10000
EXPOSE ${PORT}

CMD ["python", "-m", "src.meet_bot"]
