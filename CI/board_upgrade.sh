#!/bin/bash

export PATH=$PATH:$PWD/bin/
BOARD="arduino:avr:nano"
PORT_SERVER="/dev/ttyV0"
PORT_CLIENT="/dev/ttyV1"

if [ -n "$GITHUB_WORKSPACE" ]; then
  PROJECT_DIR = $$GITHUB_WORKSPACE
else
  PROJECT_DIR="/home/anton/coding/csad_repo/csad2125ki409krupchukap12"
fi

SERVER_SKETCH_NAME="$PROJECT_DIR/COMServer/COMServer.ino"
CLIENT_SKETCH_NAME="$PROJECT_DIR/COMClient/COMClient.ino"

echo "Uploading sketch $SERVER_SKETCH_NAME to $BOARD due $PORT_SERVER..."
arduino-cli upload -p $PORT_SERVER --fqbn $BOARD --input-dir $PROJECT_DIR/CI/build $SERVER_SKETCH_NAME

echo "Uploading sketch $CLIENT_SKETCH_NAME to $BOARD due $PORT_CLIENT..."
arduino-cli upload -p $PORT_CLIENT --fqbn $BOARD --input-dir $PROJECT_DIR/CI/build $CLIENT_SKETCH_NAME

echo "Success."