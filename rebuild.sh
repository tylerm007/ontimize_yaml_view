#/bin/bash

# This script is used to rebuild the project
# It will remove the old build directory and create a new one
# Usage: ./rebuild.sh  app_name api_endpoint (optional)
#TODO - download the app_model.yaml files first to ui/$1

function copy_seed() {
    # Copy the seed directory to the new app directory
    if [ -d "ui/$dest_dir/node_modules" ]; then
        echo "Usage: node_modules already installed"
        return 1
    fi
    echo "Copying seed directory to ui/$dest_dir"
    cp -r ui/seed/* ui/$dest_dir/
    npm install --legacy-peer-deps
}
function check_yaml_file() {
    # Check if the app_model.yaml file exists
    if [ ! -f "ui/$dest_dir/app_model.yaml" ]; then
        echo "Error: app_model.yaml file not found in ui/$dest_dir"
        exit 1
    fi
}
function rebuild_app() {
    # Rebuild the app
    check_yaml_file $app_name
    echo "Building Ontimize Application als app-build --app=$app_name"
    als app-build --app=$app_name
}

function rebuild_app_with_api() {
    # Rebuild the app with the API endpoint
    check_yaml_file $app_name
    echo "Building Ontimize Application als app-build --app=$app_name --api-endpoint=$api_endpoint"
    als app-build --app=$app_name --api-endpoint=$api_endpoint
}

################################


if [ -z "$1" ]; then
    echo "Usage: ./rebuild.sh app_name [api_endpoint (optional)]"
    exit 1
fi
als welcome
export app_name=$1
export dest_dir=$1

# Create the "$1" directory if it doesn't exist
if [ ! -d "ui/$dest_dir" ]; then
    mkdir -p "ui/$dest_dir" 
fi

copy_seed $1

if [ -z "$2" ]; then
    echo "Building Ontimize Application ui/$1 "
    rebuild_app $1
else
    echo "Building Ontimize ui/$1 with API endpoint $2"
    export api_endpoint=$2
    rebuild_app_with_api $1 $2
fi
