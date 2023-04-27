# How to Install:

Create virtual environment

```
virtualenv venv
```

Activate virtual environment
```
venv\scripts\activate
```

Install Requirements
```
pip install -r requirements.txt
```

Run project
```
python manage.py migrate
python manage.py runserver
```

Open another `terminal` but thesame project directory and run
```
celery -A hackernews worker -l info -P solo
```
