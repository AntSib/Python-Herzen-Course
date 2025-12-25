#!/usr/bin/env bash
set -e
PROTO_DIR=./proto
OUT_DIR=./app/grpc

mkdir -p $OUT_DIR
python -m grpc_tools.protoc \
  -I $PROTO_DIR \
  --python_out=$OUT_DIR \
  --grpc_python_out=$OUT_DIR \
  $PROTO_DIR/glossary.proto

# God dammit! Protoc generates one bad import:
# import glossary_pb2 as glossary__pb2
sed -i 's/^import glossary_pb2/from . import glossary_pb2/' $OUT_DIR/glossary_pb2_grpc.py

touch $OUT_DIR/__init__.py
echo "Generated protobuf code into $OUT_DIR"
