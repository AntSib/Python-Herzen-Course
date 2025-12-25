FROM python:3.12-slim

# set workdir
WORKDIR /app

# system deps (if any)
RUN apt-get update && apt-get install -y build-essential gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# generate protobuf stubs in container
RUN chmod +x ./generate_proto.sh && ./generate_proto.sh

ENV HTTP_PORT=8000
ENV GRPC_PORT=50051

# entrypoint just runs main.py which starts both uvicorn and grpc
CMD ["python", "-m", "app.main"]
