#!/bin/bash

if [ $1 = "deploy" ]
then
    echo "Deploying to title-classer web"

    cd app

    echo
    echo "Heroku login"
    heroku login

    echo
    echo "Login to container registry"
    heroku container:login

    echo
    echo "Building an image and pushing to title-classer"
    heroku container:push -a title-classer web

    echo
    echo "Releasing new title-classer"
    heroku container:release -a title-classer web

elif [ $1 = "deploy-new" ]
then
    if [ ${#2} = 0 ]
    then
        echo "The second argument must contain the name of the new application and cannot be empty"
        exit 1
    fi

    echo "Deploying new application: $2"
    
    cd app

    echo
    echo "Heroku login"
    heroku login

    echo
    echo "Creating $2"
    heroku apps:create $2

    echo
    echo "Login to container registry"
    heroku container:login

    echo
    echo "Building an image and pushing to $2"
    heroku container:push -a $2 web

    echo
    echo "Releasing new title-classer"
    heroku container:release -a $2 web

elif [ $1 = "build" ]
then
    echo "Container"

else
    echo "Argument not found; please only use arguments 'deploy' to push and release on Heroku, 'deploy-new' to create an app and push there or 'build' to build a docker container"
fi