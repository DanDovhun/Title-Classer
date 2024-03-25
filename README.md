# TitleClasser
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
```$ git clone git@github.com:AI-Project-Reexam/TitleClasser.git```

Via HTTPS:
```$ git clone https://github.com/AI-Project-Reexam/TitleClasser.git```

### Run
##### 0.) Move to the app folder: 
```cd path/to/TitleClasser/app```

#### a.) Docker
Assuming you already have docker installed on your machine, you can just follow these steps:

##### 1.) Build the image:
```$ docker build -t title_classer .```

##### 2.) Run:
```$ docker run -it -p 8000:8000 title_classer```

#### b.) Outside of Docker:
##### 1.) Get packages:
###### Get spaCy and en_core_web_sm:
```
$ pip install -U pip setuptools wheel
$ pip install -U spacy
$ python -m spacy download en_core_web_sm
```

###### Seaborn:
```$ pip install seaborn```

###### Rest of the requirements:
```$ pip install --no-cache-dir -r requirements.txt```

##### Run the application:
```$ python manage.py runserver```

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