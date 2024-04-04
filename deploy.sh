#!/bin/bash

if [ $# = 0 ]
then
    echo "Script needs at least 1 argument, please use one of these:"
    echo "'deploy' to push and release to tile-classer on Heroku (requires Dan's (the group member) login)" 
    echo "'deploy-new [APP_NAME]' to create an app and push there"
    echo "'build [IMAGE_NAME]' to build a docker container"
    echo "'run [IMAGE_NAME] [PORT]'"
fi

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
    if [ ${#2} = 0 ]
    then
        echo "The second argument must contain the name of the new docker image and cannot be empty"
        exit 1
    fi
    
    cd app
    docker build -t $2 .

elif [ $1 = "run" ]
then
    if [ $# != 3 ]
    then
        echo "The 'run' argument must be followed by [IMAGE_NAME] [PORT]"
        exit 1
    fi

    if [ ${#2} = 0 ]
    then
        echo "The second argument must contain the name of the docker image you intend to run and cannot be empty"
        exit 1
    fi

    if [ $# -lt 3 ]
    then
        echo "The third argument must contain the port for the docker container and cannot be empty"
        exit 1
    fi

    docker run -it -e "PORT=$3" -p $3:$3 $2

else
    echo "Argument not found; please only use arguments:"
    echo "'deploy' to push and release on Heroku" 
    echo "'deploy-new' to create an app and push there"
    echo "'build' to build a docker container"
fi