#! /bin/bash

# 命令路径
Django_path='/data/project/ServerProject/djangoserver'

startUwsgi(){
  # 跳转到 djangoserver 目录下，更新生成api文档
  echo -e "---cd ${Django_path} && git update--- \n"
  cd $Django_path
  # --恢复本地修改，更新代码
  git checkout .
  git pull
  sleep 1
  # 生成 django 静态文件
  echo "---python3 manage.py collectstatic---"
  python3 manage.py collectstatic
  # uwsgi启动django服务
  echo -e "\n\n ---uwsgi start django server---  \n\n"
  uwsgi --ini uwsgi/uwsgi.ini
}

stopUwsgi(){
  cd $Django_path
  uwsgi --stop uwsgi/uwsgi.pid
}

statusUwsgi(){
  cd $Django_path
  uwsgi --connect-and-read uwsgi/uwsgi.status
}

reloadUwsgi(){
  cd $Django_path
  uwsgi --reload uwsgi/uwsgi.pid
}

case "$1" in
    'start')
        startUwsgi
        ;;
    'stop')
        stopUwsgi
        ;;
    'reload')
        reloadUwsgi
        ;;
    'status')
        statusUwsgi
        ;;
    *)

    echo "Usage $0 { start | stop | status | reload }"
    exit
esac
exit 0
