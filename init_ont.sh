#/bin/bash

set -e
function init_ont() {
    # Initialize the Ontimize project
    echo "Initializing Ontimize Project"
    als app-create --app=$app_name
}

function install_node_modules() {
    # Install node modules
    echo "Installing node modules in $project_dir/ui/$app_name using npm install --force"
    cd  $project_dir/ui/$app_name
    if [ -d "node_modules" ]; then
        echo " node_modules already installed"
    else
        npm install --legacy-peer-deps 
    fi
}
if [ -z "$1" ]; then
    echo "Usage: ./init_ont.sh als_project_directory app_name"
    exit 1
fi


# Check if the project directory exists
if [ ! -d "$1" ]; then
    echo "Error: Project directory $1 does not exist."
    exit 1
fi
cd $1

# Check if the app_name is provided
if [ -z "$2" ]; then
    echo "Error: App name is required."
    exit 1
fi
source $VIRTUAL_ENV/bin/activate
als welcome
export project_dir=$1
export app_name=$2

init_ont || echo "Warning: init_ont encountered an error but continuing..."
install_node_modules