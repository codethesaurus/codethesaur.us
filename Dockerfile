FROM python:3.14-slim
ENV PYTHONBUFFERED=1
WORKDIR /code

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entrypoint script and make it executable
COPY docker-entrypoint.sh /code/
RUN chmod +x /code/docker-entrypoint.sh

# Create a non-root user and give them ownership of the code directory
RUN useradd -m django && chown -R django:django /code
USER django

# Copy the rest of the application code
COPY --chown=django:django . .

# Expose the port the app runs on
EXPOSE 8000

# Set the entrypoint script
ENTRYPOINT ["/code/docker-entrypoint.sh"]

# Default command to run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
