#/bin/bash
# Hard Coded for Mac

echo 'sh rebuild_page {python_interpreter_path} {app_path} {app_name} {api_endpoint}'
echo 'setup venv'
. $1/bin/activate
echo 'change to app_path to $2'
cd $2
cd ../..
echo 'rebuild app: $3 for api-endpoint $4'
# if $3 empty -then we skip --api-endpoint
# if $2 does not exist - we do an app-create first then app-build
als app-build --app=$3 --api-endpoint=$4