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
function install_node_modules() {
    # Install node modules
    echo "Installing node modules in $project_dir/ui/$app_name using npm install --force"
    cd  $project_dir/ui/$app_name
    if [ -d "node_modules" ]; then
        echo " node_modules already installed"
    else
        echo " starting node_modules installation"
        npm install --legacy-peer-deps 
    fi
}
echo "changing directory to $1/ui/$2"
cd $1/ui/$2
if [ "$4" = "true" ]; then
    echo "Starting npm in the background..."
    install_node_modules
    npm start &
    echo "Background process ID: $!"
fi