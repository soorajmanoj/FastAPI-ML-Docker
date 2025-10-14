# app/Dockerfile

# 1. Base Image
# Start from an official, lightweight Python image.
# 3.9-slim is good as it's small and has necessary dependencies.
FROM python:3.9-slim

# 2. Set Environment Variable (Optional but good practice)
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 3. Set Working Directory
# All subsequent commands will be executed inside this directory in the container.
WORKDIR /app

# 4. Copy Dependencies
# Copy the requirements file first. This is a Docker caching optimization:
# if requirements.txt doesn't change, Docker won't re-install dependencies.
COPY app/requirements.txt .

# 5. Install Python Dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy Model Artifacts and Application Code
# Note: Paths here are relative to the build context, which we will set as the project root.
# This copies the model artifact (trained_model.pkl) and the API code (main.py)
COPY model/trained_model.pkl .
COPY app/main.py .

# 7. Expose Port
# Inform Docker that the container will listen on port 80.
# This is documentation; we'll map a host port to this later.
EXPOSE 80

# 8. Run Command (Entrypoint)
# The default command executed when a container is started from this image.
# Uvicorn serves the 'app' object inside the 'main.py' file.
# --host 0.0.0.0 is crucial to make the server accessible from outside the container.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]