echo 'start django server'
django_path='/data/project/ServerProject/djangoserver'
uwsgi_path=${django_path}/djangoserver/uwsgi.ini
echo ${uwsgi_path}
uwsgi --ini ${uwsgi_path}

