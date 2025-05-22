FROM python:3.12-alpine

# Install dependencies
RUN apk add --no-cache gcc musl-dev libffi-dev

# Set workdir
WORKDIR /app

# Copy app files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Run using uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
