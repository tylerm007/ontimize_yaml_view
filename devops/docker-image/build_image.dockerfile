# To build image for your ApiLogicProject, see build_image.sh
#    $ sh devops/docker-image/build_image.sh .

# consider adding your version here

# ensure platform for common amd deployment, even if running on M1/2 mac --platform=linux/amd64
#FROM --platform=linux/arm64 apilogicserver/api_logic_server
#apt install net-tools
#netstat tuln 
FROM apilogicserver/api_logic_server as build

USER root
RUN apt-get update \
    && apt-get install nano \
    && export TERM=xterm \
    && apt-get install -y curl
# user api_logic_server comes from apilogicserver/api_logic_server
WORKDIR /home/api_logic_project
# USER api_logic_server
COPY ../../ .
RUN rm -rf ../../ui/yaml

# enables docker to write into container, for sqlite
RUN chown -R api_logic_server /home/api_logic_project


FROM nginx:latest

# Copy the build output to replace the default nginx contents.
#COPY --from=build /usr/local/app/dist /usr/share/nginx/html
COPY ./nginx/nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 8080

CMD [ "python", "./api_logic_server_run.py" ]