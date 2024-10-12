if [ -n "$GITHUB_WORKSPACE" ]; then
  PROJECT_DIR=$GITHUB_WORKSPACE
else
  PROJECT_DIR="/home/anton/coding/csad_repo/csad2125ki409krupchukap12"
fi

BOARD="arduino:avr:uno"
SERVER_SKETCH_NAME="$PROJECT_DIR/COMServer/COMServer.ino"
CLIENT_SKETCH_NAME="$PROJECT_DIR/COMClient/COMClient.ino"
export PATH=$PATH:$PWD/bin/

sudo apt-get install tree
tree $PROJECT_DIR

if ! command -v arduino-cli &> /dev/null
then
    echo "Arduino CLI not found. Please install Arduino CLI."
    exit 1
fi

arduino-cli core update-index

echo "Compile $SERVER_SKETCH_NAME"
arduino-cli compile --fqbn $BOARD --output-dir "$PROJECT_DIR/CI/build" $SERVER_SKETCH_NAME

echo "Compile $CLIENT_SKETCH_NAME"
arduino-cli compile --fqbn $BOARD --output-dir "$PROJECT_DIR/CI/build" $CLIENT_SKETCH_NAME

tree $PROJECT_DIR