# Tweet as Trump

Developer: Dian Yu

QA Contributions: Hanyu Cai

![alt text](https://github.com/MSIA/trump-tweets/blob/develop/figures/trump_tweet.png)

<!-- toc -->

- [Introduction](#introduction)
- [Use the app](#use-the-app)
- [Customize database connection (optional)](#customize-database-connection-optional)
  * [1. Initialize database locally](#1-initialize-database-locally)
  * [2. Initialize database in RDS instance](#2-initialize-database-in-rds-instance)
    + [Configure environment variables](#configure-environment-variables)
    + [Create database and table schema](#create-database-and-table-schema)
- [Reproduce model pipeline (optional)](#reproduce-model-pipeline-optional)

<!-- tocstop -->

## Introduction

Social media platforms have made it easier than ever for political figures and celebrities to make their voices heard. Since Donald J. Trump stepped into the White House in January 2017, he has used Twitter to criticize, praise, persuade, entertain, and establish his version of events. The platform eventually suspended his account permanently in January 2021 because of his controversial tweets. Whether one agrees or disagrees with the former president’s policies and ideas, one may be curious about what it is like to be such a controversial figure on social media and what kind of posts receive the most attention. This web application aims to offer its users the opportunity to hypothetically post tweets in the shoes of Mr. Trump and see the number of retweets they could expect to get. 

The most crucial step in this project is to train a NLP model using Mr. Trump’s previous tweets’ text and number of retweets. The datasets I used are collected and published on Kaggle by Austin Reese (https://www.kaggle.com/austinreese/trump-tweets) and Gabriel Preda (https://www.kaggle.com/gpreda/trump-tweets). I combined the two datasets to get a total of 14,219 observations of Trump's tweets during his presidency. The final model has a test Mean Absolute Percentage Error (MAPE) of 37.6%. 

## Directory structure 

```
├── README.md                         <- You are here
├── app
│   ├── static/                       <- CSS, JS files that remain static
│   ├── templates/                    <- HTML (or other code) that is templated and changes based on a set of inputs
│   ├── boot.sh                       <- Start up script for launching app in Docker container.
│   ├── Dockerfile                    <- Dockerfile for building image to run app  
│
├── config                            <- Directory for configuration files 
│   ├── local/                        <- Directory for keeping environment variables and other local configurations that *do not sync** to Github 
│   ├── logging/                      <- Configuration of python loggers
│   ├── flaskconfig.py                <- Configurations for Flask API
│   ├── config.yaml                   <- Configurations for model pipeline
│
├── data                              <- Folder that contains data used or generated. Only the external/ and sample/ subdirectories are tracked by git. 
│   ├── raw/                          <- Raw data downloaded from Kaggle
│   ├── external/                     <- NLTK data
│   ├── pipeline/                     <- Data artifacts created in model pipeline
│   ├── tweets.db                     <- SQLite database
│
├── deliverables/                     <- Presentation slides 
│
├── figures/                          <- Figures for documentation
│
├── models/                           <- Trained model objects (TMOs), model predictions, and model summaries
│
├── src/                              <- Source data for the project 
│
├── test/                             <- Files necessary for running model tests (see documentation below) 
│
├── app.py                            <- Flask wrapper for running the model 
│
├── run.py                            <- Simplifies the execution of the src scripts 
│
├── requirements.txt                  <- Python package dependencies 
│
├── Dockerfile                        <- Dockerfile for building image to create database and run model pipeline
```

## Use the App
```bash
make tweet
```

Once the app starts running, you may copy and paste this URL http://0.0.0.0:5000/ to a browser and start using the app. 

## Customize database connection (optional)
Starting from here, all the sections below are completely optional.

### 1. Initialize database locally
By default, the text you enter and its predicted number of retweets are saved in the `data/tweets.db` SQLite database already initialized for you. 

You can also initialize your own local SQLite database by providing a customized engine (SQLAlchemy connection string) string. The default engine string is `sqlite:///data/tweets.db`.

```bash
docker build -f Dockerfile -t tweets_data .
docker run --mount type=bind,source="$(pwd)",target=/app tweets_data python3 run.py create_db \
    --engine_string={your_engine_string}
```

### 2. Initialize database in RDS instance
This project also provides the possibility to connect to your database in an AWS RDS instance:

#### Configure environment variables
To configure MYSQL-related environment variables:
```bash
export MYSQL_USER="YOUR_USERNAME"
export MYSQL_PASSWORD="YOUR_PASSWORD"
export MYSQL_HOST="YOUR_HOST"
export MYSQL_PORT="YOUR_PORT"
export DATABASE_NAME="YOUR_DATABASE"
```
where `"YOUR_HOST"` should point to the RDS instance.

#### Create database and table schema
To use the docker image to create database and table schema on RDS:
```bash
docker build -f Dockerfile -t tweets_data .
docker run -it \
    -e MYSQL_HOST \
    -e MYSQL_PORT \
    -e MYSQL_USER \
    -e MYSQL_PASSWORD \
    -e DATABASE_NAME \
    tweets_data run.py create_db
```

Then, to run the app with the database on RDS:
```bash
docker run \
    -e MYSQL_HOST \
    -e MYSQL_PORT \
    -e MYSQL_USER \
    -e MYSQL_PASSWORD \
    -e DATABASE_NAME \
    -p 5000:5000 tweets_app
```
Once the app starts running, you may copy and paste this URL http://0.0.0.0:5000/ to a browser and start using the app. Your text inputs and their corresponding predictions will be saved in the specified RDS database.

## Reproduce model pipeline (optional)
If you wish, you can easily re-run the model pipeline:
```bash
make pipeline
```

This will `read` the data from the `data/raw` folder, `process` the texts in the data, `clean` the data, and `train` the neural network model. The trained model objects along with model performance metric will be saved in the `model` folder.