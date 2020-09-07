# 服务器shell文件中使用uwsgi管理django服务

### **`uwsgi`**核心命令

启动uwsgi服务
> `uwsgi --ini uwsgi.ini`

重启uwsgi服务
> `uwsgi --reload uwsgi/uwsgi.pid`

查看uwsgi状态
> `uwsgi --connect-and-read uwsgi/uwsgi.status`

停止uwsgi服务
> `uwsgi --stop uwsgi/uwsgi.pid`

***使用`uwsgi`管理`django`服务的好处：***

**不需要自己管理`django`服务的进程，`uwsgi`会自己保存到`uwsgi/uwsgi.pid`文件中**


### **shell**命令文件

```
#! /bin/bash

# 命令路径
Django_path='/data/project/ServerProject/djangoserver'

gitUpdate(){
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
}

startUwsgi(){
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
  # uwsgi启动django服务
  echo -e "\n\n ---uwsgi reload django server---  \n\n"
  uwsgi --reload uwsgi/uwsgi.pid
}

case "$1" in
    'start')
        gitUpdate
        startUwsgi
        ;;
    'stop')
        stopUwsgi
        ;;
    'reload')
        gitUpdate
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

```

### 
