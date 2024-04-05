# TitleClasser
Address: https://title-classer-43bc9ae7d642.herokuapp.com/
## Description
The purpose of this project is to automate classification of articles into a specific category. The size of the text can vary from the first paragraph to the entire article. 

Our labels are:
* 0 (Politics)
* 1 (Sport)
* 2 (Technology)
* 3 (Entertainment)
* 4 (Business)

To classify the articles we're using logistic regression with the help One-vs-Rest method since the output isn't a simple binary classification of yes or no, a placemement into one of 5 labels.

## Run
### 1.) Clone directory
Via SSH:
```
git clone git@github.com:AI-Project-Reexam/TitleClasser.git
```

Via HTTPS:
```
git clone https://github.com/AI-Project-Reexam/TitleClasser.git
```

### Run
##### Move to the app folder: 
```
cd path/to/TitleClasser/app
```

#### a.) Docker
Assuming you already have docker installed on your machine, you can just follow these steps:
##### Build your own container
##### 1.) Build the image:
```
// Pull python:3.11 image
docker pull python:3.11

// Build title_classer image
docker build -t title_classer .
```

##### 2.) Run:
```
docker run -it -e "PORT=8000" -p 8000:8000 title_classer:latest
```

#### b.) Outside of Docker:
##### 0.) Create Conda environment
```
// Create venv
conda create -n title-classer

// Activate
conda activate title-classer
```
##### 1.) Get packages:
###### Get packages that had issues being in requirements.txt:
```
pip install -U pip setuptools wheel
pip install -U spacy
python -m spacy download en_core_web_sm 
python -m pip install tensorflow
pip install seaborn
```

###### Rest of the requirements:
```
pip install --no-cache-dir -r requirements.txt
```

##### Run the application:
```
python manage.py runserver
```

## Deployment on Heroku:
### Deployment:
Address: *See the address on top of the document*
### Login to Heroku:
```
heroku login
```

### Login to Heroku's Container Registry:
```
heroku container:login
```

### Create app:
_We already took this name and the name won't work for anyone else if they try running this command verbatim. This is only to demonstrate how the application was created in Heroku_
```
heroku apps:create title-classer
```

### Build, push and deploy Docker container:
```
// Build and push the container
heroku container:push -a title-classer web

// Deploy the container
heroku container:release -a title-classer web
```

When the container is deployed the app will restart will take about 60 seconds to be running again.

## Using the Shell Script
There is a shell script located in the root of the repository named *deploy.sh*. This shell script was added to streamline building and running the docker image and deploying the docker image to Heroku. To run the script use these commands:
```
// Make the script executable:
chmod +x deploy.sh

// Run the script:
./deploy.sh [ ARGUMENT_1 ]
```

The arguments are necessary to run the script so it would know which set of commands it should run. Here are the accepted arguments:

*NOTE: some arguments must be followed by another to work*
* ```--deploy```
    * Push a docker containter to Heroku and release it on the title-classer app on heroku
    * This should and can only be by the group

* ```--deploy-new [ APP_NAME ]```
    * Create your own app on Heroku and deploy a container there

* ```--build [IMAGE_NAME]```
    * Build a Docker image on your machine

* ```--run [ IMAGE_NAME ] [ PORT ]```
    * Run the Docker image

__NOTE:__ *This is an UN*X shell script, while it may work on Linux or Mac, it may not work on Windows' native command line*

## Tools and Technologies:
* Website:
    * Django
    * SQLite

* Preprocessing:
    * spaCy
    * en_core_web_sm

* AI Model:
    * Pandas
    * SQLite
    * scikit-learn
    * Tensorflow
    * Numpy

## Contributors:
* Aditya Nair
* Daniel Dovhun
