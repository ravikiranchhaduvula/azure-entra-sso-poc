FROM python:3.13-slim

# Prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Show Python logs immediately
ENV PYTHONUNBUFFERED=1

# Working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose application port
EXPOSE 8000

CMD sh -c "python manage.py migrate && python manage.py seed_demo_user && python manage.py runserver 0.0.0.0:8000"