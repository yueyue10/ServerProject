#! /bin/bash
### cd命令不管用: dos2unix node.sh node.sh
### forever日志目录: /root/.forever/
time_str=$(date "+%Y-%m-%d %H:%M:%S")
# 输出时间标识
echo ---current time $time_str---
# 命令路径
Express_Path='/data/project/ServerProject/expressServer/'
# 跳转到expressServer目录下，更新生成api文档
echo -e "---cd ${Express_Path} && git update && apidoc create doc--- \n"
cd $Express_Path
# --恢复本地修改，更新代码
git checkout .
git pull
sleep 1
# --移动doc下的package.json到项目根目录下
sudo mv doc/package.json ./
apidoc -i routes/ -o public/apidoc/
sleep 1
# 跳转到expressServer/bin目录下，查找www文件
cd ${Express_Path}bin/
express_file=`ls`

# 判断forever是否存在www
getForever(){
  forever_list=`forever list`
  # echo ---forever_list $forever_list---
  # 判断是否存在www服务
  filter="www"
  result=$(echo $forever_list | grep "${filter}")
  if [[ "$result" != "" ]]
  then
      echo "---forever_list include $filter---"
      return 1
  else
      echo "---forever_list not include $filter---"
      return 0
  fi
}

# 如果文件夹中是否存在www，存在表示进入文件夹成功
if [ $express_file = "www" ];then
   echo -e "---\n cd ${Express_Path}bin/ && forever start server--- \n"
   rm -rf /root/.forever/forever.log
   getForever
   www_result=$?
   echo -e "---www_result $www_result---"
   if [ $www_result == 1 ];then
     echo "---restart www---"
     forever restart -l forever.log www
   else
     echo "---start www---"
     forever start -l forever.log www
   fi
fi

#echo -e `forever start -l ${time_str}.log /data/project/ServerProject/expressServer/bin/www`
# rm -rf /root/.forever/forever.log
