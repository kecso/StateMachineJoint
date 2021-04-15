# Only use these steps if you want a standalone execution of the image, otherwise look at the docker-compose.yml
# Build a and run docker image for this repository
# 1. make sure docker is installed
# 2. make sure you have a clean copy of this repository (no npm install was done on the project yet)
# 3. go to the directory where this file exists (the root of your repo)
# 4. $ docker build -t webgme-server .
# 5. $ docker run -d -p 8888:8888 -v /var/run/docker.sock:/var/run/docker.sock --link mongo:mongo webgme-server


# Node 14
FROM node:fermium
MAINTAINER Tamas Kecskes <tamas.kecskes@vanderbilt.edu>
# on top of node we need Python
RUN apt-get update && \
    apt-get install -y git\
        apt-transport-https \
        python \
        python-pip \
        python3-pip \
        python-setuptools
# we also need the latest webgme-bindings to be able to run python plugins
RUN pip install webgme_bindings
RUN pip3 install webgme-bindings

# just creating the directories where our webgme server will run
RUN mkdir /usr/app
WORKDIR /usr/app

# copy app source
ADD config /usr/app/config/
ADD src /usr/app/src/
ADD package.json /usr/app/
ADD webgme-setup.json /usr/app/
ADD app.js /usr/app/

# Install node-modules
RUN npm install
 
CMD ["npm", "start"]
