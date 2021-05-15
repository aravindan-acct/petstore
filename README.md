# Introduction

This is the API server for the petstore application. It connects to a mysql db for storing data.

## Important note

There is a provisioning script in this repo called "provisioning.sh" which sets up the mysql db locally for the API server. Please ensure that you edit the script and change the mysql credentials in the script before using it. 

The provisioning script is provided for deployment on Ubuntu based systems. Please make necessary changes to the script if any other operating system is used.

## Usage

`git clone https://github.com/aravindan-acct/petstore.git`

`cd petstore`

`sudo bash provisioning.sh`

At this time, your server should be running and listening on port 8080.

Access the API documentation / swagger page by accessing: 

`http://<ip>:8080/api/petstore/1.0.0/ui/#`

For connecting a front end web tier application to this API, checkout https://github.com/aravindan-acct/frontend_UI_app

