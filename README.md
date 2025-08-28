# OCR / DA Python - Project12

## Epic Events

Build a secure backend architecture with Python and SQL

A CLI application allowing three different type of users to connect
(permissions management) and to manage customers, contracts and events

### Introduction

These instructions allow you to :
- get the program
- install the required environment
- run and use it

---
### Requirements

1. modules
```
python 3.10, python3.10-venv, git, pipenv,  
SQLAlchemy, mysql-connector-python, passlib, argon2, simple-term-menu, sentry-sdk
```

2. applications
```
mysql-server-8.0, mysql-client
```
You'll need to create a dedicated DB and user to your application

### Installation

1. Clone this repo and go in the project's directory

2. Create the virtual environment and install dependencies
```
pipenv sync
```
3. Enter the venv
```
pipenv shell
```
4. Setup your database  

Once your MySQL server is installed and running :
- connect with the root user  
```
mysql -u root -p
```
- create a database  
```
CREATE DATABASE MYDB
```
- create user and grant permissions  
```
CREATE USER 'MYUSER'@'%' IDENTIFIED BY 'MYPASSWORD'; 
GRANT ALL PRIVILEGES ON MYDB TO 'MYUSER'@'%';
```

5. Create your configuration's file  

Create a file named `config.py` in your app's directory containing (at least):
```
USER = your_db_user
PASSWORD = your_db_user_password
```

6. Sentry  

This app can use Sentry. You just have to place the server's URL containing your 
key in the `config.py` file :
```
SENTRY_URL = your_url
```
---
### Execution

1. Go into the app directory

2. Launch the app
```
python main.py
```

___
### Usage

1. First connection  
Connect first with the default 'admin' user and 'password' as password, then create new collaborators following the menu  
 

2. Users  
There are three roles having three kinds of permissions. The menu is launched accordingly depending on the type of user logged in.  
First level is objects (Collaborators, Customers, Contracts, Event), second level is CRUD depending on permissions, and there are some filter on 'list'.
-----
### Author

YaL  <yann@needsome.coffee>

### License

MIT License  
Copyright (c) 2025 

