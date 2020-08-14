echo 'start django server'
django_path='/data/project/ServerProject/djangoserver'
nohup python ${django_path}/manage.py runserver 0.0.0.0:8080 > /root/.django/run.log 2&>1 &
