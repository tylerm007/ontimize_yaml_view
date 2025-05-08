#/bin/bash

# This script is used to rebuild the project
# It will remove the old build directory and create a new one
# Usage: ./rebuild.sh als_path app_name api_endpoint (optional)
#TODO - download the app_model.yaml files first to ui/$2
if [ -z "$1" ]; then
    echo "Usage: ./rebuild.sh als_path app_name api_endpoint (optional)"
    exit 1
fi
cd $1
echo als --version
if [ -z "$2" ]; then
    echo "Usage: ./rebuild.sh als_path app_name api_endpoint (optional)"
    exit 1
fi
cd ui/$2
npm install
cd ../..
if [ -z "$3" ]; then
    echo "Building Ontimize Application ui/$2 "
    als app-build --app=$1
else
    echo "Building Ontimize ui/$2 with API endpoint $3"
    als app-build --app=$2 --api-endpoint=$3
fi
