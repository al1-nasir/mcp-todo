FROM python:3.9-slim

WORKDIR /app

# Copy server code only
COPY app.py /app/app.py

# Expose port
EXPOSE 8765

CMD ["python", "app.py"]

