FROM python:3.12-slim
WORKDIR /app
COPY 06_code/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY 06_code /app
ENV PORT=5000
ENV FLASK_DEBUG=0
RUN mkdir -p /app/storage/uploads
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "120", "backend.wsgi:app"]
