使用shell命令启动django服务

### django.sh内容

```
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
```

### shell核心代码

跳转到`djangoserver`目录下，更新代码
> `cd $Django_path`
> `git checkout .`
> `git pull`

生成`apidoc`文档
> `python3 manage.py collectstatic`

关闭`django`服务的8080端口
> `finishPort`

使用`uwsgi`启动`django`
> `uwsgi --ini ${uwsgi_path}`

---
其中比较麻烦的地方就是`finishPort()`方法，查找被占用的8080端口并杀掉。

* 1.使用**``netstat -anp|grep 8080``**命令得到占用端口信息的`字符串`,`for循环`遍历
字符串并添加到`array数组`里面。
![](https://p1-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/d9ec142befc445a3842e53f20ee0f944~tplv-k3u1fbpfcp-zoom-1.image)

* 2.查找`array数组`里面的第六项的`端口字符串`,并获取`符号/`的位置并截取端口的值`$port`。

* 3.使用`sudo kill -9 $port`命令关闭8080端口占用的进程。

### **`uwsgi.ini`**代码

```
[uwsgi]
chdir = /data/project/ServerProject/djangoserver
module = djangoserver.wsgi
socket = :8080
master = true
processes = 4
vacuum = true

stats=%(chdir)/uwsgi/uwsgi.status
pidfile=%(chdir)/uwsgi/uwsgi.pid
```

### 常用shell命令

输出到日志到窗口
> `echo -e "---python3 ...---`

变量定义,使用
> `Django_path='/data/...'`  `${Django_path}` `$Django_path`


