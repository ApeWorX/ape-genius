# Use the specific version of Python
FROM python:3.10.6

# Set the working directory in the container
WORKDIR /app

# Copy the Python requirements file into the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code into the container at /app
COPY . /app/

# Run bot.py when the container launches
CMD ["python", "bot.py"]