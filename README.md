# Ensemble_Backend_Project_IfrazAhmed


API to manage, search and like/dislike movies.

# Setup Guide

```
# Activate venv
$ pipenv shell

# Install Dependencies
$ pipenv install

# Create DataBase
$ python3
>> from main import db
>> db.create_all()
>> exit()

# Run Server (http://localhost:5000)
python3 main.py
```
