# Use an appropriate base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the dataset file to the app
# Ensure spaces are handled by using quotes and specifying the exact path
COPY "cloudfarm_app/filled_crop_fertilizer_dataset-filled_crop_fertilizer_dataset.csv.csv" /app/cloudfarm_app/

# Copy the rest of your app code (ensure all the files are copied)
COPY . /app/

# Apply database migrations
RUN python manage.py migrate

# Collect static files (if any)
RUN python manage.py collectstatic --noinput

# Expose port and run the app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
