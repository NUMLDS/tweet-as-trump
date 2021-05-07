# Tweet as Trump

Developer: Dian Yu

QA Contributions: Hanyu Cai

![alt text](https://github.com/MSIA/2021-msia423-yu-dian-project/blob/develop/figures/trump_tweet.png)

<!-- toc -->

- [Project charter](#project-charter)
  * [1. Vision](#1-vision)
  * [2. Mission](#2-mission)
  * [3. Success criteria](#3-success-criteria)
- [Directory structure](#directory-structure)
- [Data acquisition](#data-acquisition)
  * [1. Download raw data from Kaggle](#1-download-raw-data-from-kaggle)
  * [2. Build Docker image](#2-build-docker-image)
  * [3. Connect to Northwestern VPN](#3-connect-to-northwestern-vpn)
  * [4. Load data into S3 bucket](#4-load-data-into-s3-bucket)
    + [Configure S3 credentials](#configure-s3-credentials)
    + [Upload file to S3](#upload-file-to-s3)
  * [5. Initialize database locally](#5-initialize-database-locally)
  * [6. Initialize database in RDS instance](#6-initialize-database-in-rds-instance)
    + [Configure environment variables](#configure-environment-variables)
    + [Create database and table schema](#create-database-and-table-schema)

<!-- tocstop -->

## Project charter

### 1. Vision

Social media platforms have made it easier than ever for political figures and celebrities to make their voices heard. Since Donald J. Trump declared his candidacy in June 2015, he has used Twitter to criticize, praise, persuade, entertain, and establish his version of events.  Whether one agrees or disagrees with the former president’s policies and ideas, one may be curious about what it is like to be such a controversial figure on social media and what kind of posts receive the most attention. This web application aims to offer its users the opportunity to hypothetically post tweets in the shoes of Mr. Trump and see the number of favorites and retweets they could expect to get. After having fun trying different tweets on the app, the users would hopefully think a little more about the controversial and inciting nature of social media posts.

### 2. Mission
The final web app would enable the user to enter a tweet—a small paragraph with less than 280 characters. After the user finishes, the app would output the predicted number of retweets if Mr. Trump tweeted the message.

The most crucial step in this project is to train a model using Mr. Trump’s previous tweets’ retweets data. The dataset I selected is collected and published on Kaggle by Austin Reese (https://www.kaggle.com/austinreese/trump-tweets). For data pre-processing and model architecture, I expect to apply Natural Language Processing (NLP) techniques, including but not limited to tokenization, embeddings, and long short-term memory (LSTM) models. The final model would take a string of any length smaller than 280 characters as an input and output the predicted number of retweets.

It is also worthy of mentioning that the model developed in this project is readily applicable to social media strategy making. It is easy to retrain the model using a new celebrity or policy maker’s social media data. Then, before the user and his/her social media team publish a new post, they can use the application to select the appropriate topic and wording that would attract the most attention. This possibility is not part of my core vision but makes monetization reasonably easy.

### 3. Success criteria

#### Machine learning performance metric

I think Mean Absolute Percentage Error (MAPE) is a good metric for the machine learning model. For example, if the model predicts 1.2 million retweets for a tweet with 1 million retweets, the Absolute Percentage Error for this point is 20%. I expect predicting the number of retweets using only tweet content to be a relatively challenging problem since many other factors determine retweets, such as time of the day and recent events. Thus, I am willing to view a MAPE smaller than 40% as an indication that a model is ready to go live. Although R-squared is also a standard metric for a regression problem like this one, I decide to use MAPE because it is much easier to explain to non-technical audiences.

#### Business outcome metric

Since the web app’s purpose is to create a fun user experience, Daily Active User (DAU) is a great metric to measure user engagement. I expect most users to be one-time users, but I am not worried about growth. Many users will likely share screenshots of their creative tweets on social media and thus introduce more users to the app, creating a positive feedback loop. If the DAU reaches a level high enough, it is reasonable to monetize via advertisements.

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
│
├── data                              <- Folder that contains data used or generated. Only the external/ and sample/ subdirectories are tracked by git. 
│   ├── raw/                          <- Raw data downloaded from Kaggle, will be synced with git
│   ├── external/                     <- External data sources, usually reference data,  will be synced with git
│   ├── sample/                       <- Sample data used for code development and testing, will be synced with git
│
├── deliverables/                     <- Any white papers, presentations, final work products that are presented or delivered to a stakeholder 
│
├── docs/                             <- Sphinx documentation based on Python docstrings. Optional for this project. 
│
├── figures/                          <- Generated graphics and figures to be used in reporting, documentation, etc
│
├── models/                           <- Trained model objects (TMOs), model predictions, and/or model summaries
│
├── notebooks/
│   ├── archive/                      <- Develop notebooks no longer being used.
│   ├── deliver/                      <- Notebooks shared with others / in final state
│   ├── develop/                      <- Current notebooks being used in development.
│   ├── template.ipynb                <- Template notebook for analysis with useful imports, helper functions, and SQLAlchemy setup. 
│
├── reference/                        <- Any reference material relevant to the project
│
├── src/                              <- Source data for the project 
│   ├── add_tweets.py/                <- Python script for creating database and adding data
│   ├── s3.py/                        <- Python script for uploading raw data to S3
│
├── test/                             <- Files necessary for running model tests (see documentation below) 
│
├── app.py                            <- Flask wrapper for running the model 
├── run.py                            <- Simplifies the execution of one or more of the src scripts  
├── requirements.txt                  <- Python package dependencies 
├── Dockerfile                        <- Dockerfile for building image to upload data to s3 and create database
```

## Data acquisition
### 1. Download raw data from Kaggle
To download the data used for this app, go to the [Trump Tweets dataset page](https://www.kaggle.com/austinreese/trump-tweets?select=realdonaldtrump.csv) on Kaggle. Click on the download button on the top right, and unzip the downloaded zip file. We will only use the `realdonaldtrump.csv` dataset, a copy of which is synced to `data/raw/` folder in the project directory.

### 2. Build Docker image
To build the Docker image for data acquisition, run the command below in the project root directory:
```bash
docker build -f Dockerfile -t tweets_data .
```

### 3. Connect to Northwestern VPN
For more information about how to connect to Northwestern's VPN, click the link [here](https://www.it.northwestern.edu/oncampus/vpn/index.html).

### 4. Load data into S3 bucket
#### Configure S3 credentials
To load S3 credentials as environment variables:
```bash
export AWS_ACCESS_KEY_ID="YOUR_ACCESS_KEY_ID"
export AWS_SECRET_ACCESS_KEY="YOUR_SECRET_ACCESS_KEY"
```

#### Upload file to S3
To upload the `realdonaltrump.csv` file to a configurable S3 bucket:
```bash
docker run -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY tweets_data src/s3.py --s3path={your_s3_path}
```
where `{your_s3_path}` should be your S3 file path to upload the data. The default for the option is `"s3://2021-msia423-yu-dian/realdonaldtrump.csv"`

You may also specify the `--local_path` option, the default of which is `"data/raw/realdonaldtrump.csv"`:
```bash
docker run -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY tweets_data src/s3.py --s3path={your_s3_path} --local_path={your_local_path}
```

### 5. Initialize database locally
A local SQLite database can be created for development and local testing. 
```bash
docker run -it tweets_data run.py create_db
```

The default engine string (SQLAlchemy connection string) to the database file is `sqlite:///data/tweets.db`, where the three `///` denote that it is a relative path to where the code is being run (which is from the root of this directory). 

You can provide a customized engine string as an environment variable:
```bash
export SQLALCHEMY_DATABASE_URI="YOUR_ENGINE_STRING"
docker run -it -e SQLALCHEMY_DATABASE_URI tweets_data run.py create_db
```

### 6. Initialize database in RDS instance
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
docker run -it \
    -e MYSQL_HOST \
    -e MYSQL_PORT \
    -e MYSQL_USER \
    -e MYSQL_PASSWORD \
    -e DATABASE_NAME \
    tweets_data run.py create_db
```
