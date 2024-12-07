#/bin/bash
echo change dir to $1
cd $1
cd ../..
echo rebuild app: $2 for api-endpoint $3
als app-build --app=$2 --api-endpoint=$3