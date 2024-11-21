# Only use these steps if you want a standalone execution of the image, otherwise look at the docker-compose.yml
# Build a and run docker image for this repository
# 1. make sure docker is installed
# 2. make sure you have a clean copy of this repository (no npm install was done on the project yet)
# 3. go to the directory where this file exists (the root of your repo)
# 4. $ docker build -t webgme-server .
# 5. $ docker run -d -p 8888:8888 -v /var/run/docker.sock:/var/run/docker.sock --link mongo:mongo webgme-server


# Node 14
FROM node:20.18.1-alpine3.20
# on top of node we need Python
RUN apk update
RUN apk add --no-cache make g++ git python3 py3-pip py3-setuptools dotnet6-sdk pythonispython3
RUN pip3 install --break-system-packages webgme-bindings lark

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
