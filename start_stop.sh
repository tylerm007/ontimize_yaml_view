#/bin/bash

# Ensure exactly 4 arguments are passed
if [ "$#" -ne 4 ]; then
    echo "Error: This script requires exactly 4 arguments."
    echo "Usage: $0 <project_directory> <file_path> <port> <start_flag>"
    exit 1
fi

echo "Project Directory: $1"
echo "ui/File Path: $2"
echo "Stop Ontiimize on Port: $3"
echo "Start Flag: $4"
# Check if the project port is running
process_id=$(lsof -ti :$3)
if [ -n "$process_id" ]; then
    echo "Process ID: $process_id"
    echo "Port $3 is already in use. Killing process..."
    kill -9 $process_id
fi

echo "changing directory to $1/ui/$2"
cd $1/ui/$2
if [ "$4" = "true" ]; then
    echo "Starting npm in the background..."
    #npm install moment --force
    npm start &
    echo "Background process ID: $!"
fi