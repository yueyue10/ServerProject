#! /bin/bash
### cd命令不管用: dos2unix test.sh test.sh

cdTest(){
  # 进入ftp目录
  cd /data/ftp
  # 查看目录下所有文件
  # echo `ls`
  for i in `ls`
  do
  echo $i;
  done
}

dateTest(){
  # 查看当前日期
  echo `date`
  # 输出格式化的日期
  time3=$(date "+%Y-%m-%d_%H:%M:%S")
  echo ---$time3---
}

foreverTest(){
  # 查看forever开启的服务
  forever_list=`forever list`
  echo ---forever_list $forever_list---
  # 判断是否存在www服务
  s2="www"
  result=$(echo $forever_list | grep "${s2}")
  if [[ "$result" != "" ]]
  then
      echo "$forever_list include $s2"
  else
      echo "$forever_list not include $s2"
  fi
}


checkType(){
# 方法传参：https://blog.csdn.net/happyhorizion/article/details/80431327
# 条件判断、参数以及变量替换 https://www.cnblogs.com/wangkongming/p/4936825.html
  echo $1
  echo $1|grep [a-zA-Z]>/dev/null
  if [ $? -eq 0 ];then
  echo "string"
  else
  echo "data"
  fi
}

forTest(){
  port_comd=`netstat -anp|grep 8080`
  echo $port_comd
  port=${port_comd[0]}
  echo $port
}

portTest(){
# for循环参考：https://www.cnblogs.com/EasonJim/p/8315939.html
# for循环参考：https://www.cnblogs.com/machangwei-8/p/8457496.html
# 端口占用参考：https://www.cnblogs.com/pretty-ru/p/10906560.html
# 端口占用参考：https://www.cnblogs.com/sench/p/8903138.html
# array数组方法:https://blog.csdn.net/asty9000/article/details/87103111
# 字符串操作:https://www.cnblogs.com/gaochsh/p/6901809.html
#  sudo lsof -i:8080
#  fuser -v -n tcp 8080
#  netstat -anp|grep 8080

  array=()
  for i in `netstat -anp|grep 8080`
    do
#    echo $i;
     array+=($i)
    done
#  echo "${array[@]}"
  prot_str=${array[6]}
#  echo $prot_str
  port_index=`expr index ${prot_str} "/"`
  echo $port_index
  port=${prot_str:0:port_index-1}
  echo $port
  return $port
}

finishPort(){
  port=`portTest`
  echo "${port} 123"
  if [ ! -n "$para1" ]; then
    echo "$port is NULL"
  else
    sudo kill -9 $port
    echo "close $port"
  fi
}

#cdTest
#portTest
finishPort
