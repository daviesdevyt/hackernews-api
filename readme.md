How to Install:

Create virtual environment

Run 'pip install -r requirements.txt'
Run 'python manage.py migrate'

Open another terminal but thesame project directory
Run 'celery -A hackernews worker -l info -P solo'