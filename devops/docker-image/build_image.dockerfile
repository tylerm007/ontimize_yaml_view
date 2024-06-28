# To build image for your ApiLogicProject, see build_image.sh
#    $ sh devops/docker-image/build_image.sh .

# consider adding your version here

FROM node:latest


WORKDIR ../../ui/yaml
#RUN npm install
ENV NODE_ENV=container

#RUN chown -R node /opt/app

# ensure platform for common amd deployment, even if running on M1/2 mac --platform=linux/amd64

# FROM apilogicserver/api_logic_server  
FROM --platform=linux/amd64 apilogicserver/api_logic_server
USER root

WORKDIR /home/api_logic_project
# USER api_logic_server
COPY ../../ .

# user api_logic_server comes from apilogicserver/api_logic_server

RUN chown -R api_logic_server /home/api_logic_project

#CMD [ "python", "./api_logic_server_run.py" ]
# Install dependencies and build your application
#RUN npm start
CMD ["tail", "-f", "/dev/null"]