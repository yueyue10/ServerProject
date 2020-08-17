#! /bin/bash
finishPort(){
  array=()
  for i in `netstat -anp|grep 8080`
    do
     array+=($i)
    done
  # 判断端口是否被占用
  if [ ! -n "$array" ]; then
    echo "---8080 is not use---"
  else
    echo "---port data_array $array ---"
    prot_str=${array[6]}
    port_index=`expr index ${prot_str} "/"`
    echo "---fint port_pid_index $port_index ---"
    port=${prot_str:0:port_index-1}
    echo "---fint port_pid $port ---"
    sudo kill -9 $port
    echo "--- kill port_pid $port ---"
  fi
}
echo '---start django server---'
# 命令路径
Django_path='/data/project/ServerProject/djangoserver'
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
uwsgi_path=${Django_path}/djangoserver/uwsgi.ini
finishPort
echo -e "\n\n ---uwsgi start django server---  \n\n"
uwsgi --ini ${uwsgi_path}
