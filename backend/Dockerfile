FROM python:3.9

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Install pymongo with the srv extra
RUN pip install "pymongo[srv]"

# Copy the rest of the application
COPY . .

# Run the application
CMD ["celery", "-A", "tasks", "worker", "--loglevel=info"]
