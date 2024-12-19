# Stage 1: Build the Vite project
FROM node:23-alpine AS build-stage

WORKDIR /app

# Copy the package.json and package-lock.json
COPY . /app

# Install dependencies
COPY frontend/package.json /app
COPY frontend/package-lock.json /app
RUN npm --prefix frontend install

# Build the Vite project
RUN npm --prefix frontend run build

# Stage 2: Run the FastAPI app
FROM python:3.12-alpine

WORKDIR /app


# Copy the FastAPI app
COPY ./* /app

# Install FastAPI and Uvicorn
RUN pip install pydantic-settings
RUN pip install -r requirements.txt

# Expose the port FastAPI will run on
EXPOSE 8000

# Command to run the FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]