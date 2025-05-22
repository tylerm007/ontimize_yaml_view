#/bin/bash

# This script is used to rebuild the Ontimize project
# Usage: ./rebuild.sh  app_name [api_endpoint (optional)]
#TODO - download the app_model.yaml files first to ui/$1
set -e
function copy_seed() {
    # Copy the seed directory to the new app directory
    echo "Copying seed directory to ui/$dest_dir"
    cp -r ui/seed/* ui/$dest_dir/
    if [ -d "ui/$dest_dir/node_modules" ]; then
        echo " node_modules already installed"
    else
        echo "Installing node modules in ui/$dest_dir using npm install --force"
        npm install --legacy-peer-deps
    fi
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

################################main code#####################################


if [ -z "$1" ]; then
    echo "Usage: ./rebuild.sh app_name [api_endpoint (optional)]"
    exit 1
fi
source $VIRTUAL_ENV/bin/activate
als welcome
export app_name=$1
export dest_dir=$1

# Create the "$1" directory if it doesn't exist
if [ ! -d "ui/$dest_dir" ]; then
    mkdir -p "ui/$dest_dir" 
else
    # remove the existing application pages
    echo "Removing existing application in ui/$dest_dir/src/app"
    #rm -rf ui/$dest_dir/src/app/main
fi

#copy_seed $1

if [ -z "$2" ]; then
    echo "Building Ontimize Application ui/$1 "
    rebuild_app $1
else
    echo "Building Ontimize ui/$1 with API endpoint $2"
    export api_endpoint=$2
    rebuild_app_with_api $1 $2
fi
