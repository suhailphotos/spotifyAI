# Base image for Python
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies for Python
RUN apt-get update && apt-get install -y curl

# Install Poetry for Python dependency management
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
ENV PATH="/root/.local/bin:$PATH"

# Copy dependency files first to leverage Docker caching
COPY pyproject.toml poetry.lock ./

# Install project dependencies using Poetry
RUN poetry install --no-dev

# Copy application source code
COPY src/ /app/src
COPY tests/ /app/tests

# Expose Flask's default port
EXPOSE 5000

# Default command to run the Flask app
CMD ["poetry", "run", "python", "src/spotifyai/app.py"]
