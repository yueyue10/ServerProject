echo 'start django server'
django_path='/data/project/ServerProject/djangoserver'
uwsgi_path=${django_path}/djangoserver/uwsgi.ini
nohup uwsgi --ini ${uwsgi_path} > /root/.django/run.log 2&>1 &
echo ${uwsgi_path}
