# experssServer项目
express服务项目
>项目已经部署到：http://81.68.145.189:3000/apidoc/
* https域名的地址：https://passionboy.xyz/express/apidoc/ 这个地址下的接口测试有问题

>/doc/package.json 是备份文件，上传到服务器使用。因为服务器不需要动态更新服务，本地测试才需要。
* 去掉了[browser-sync]
* 去掉了[gulp]
* 去掉了[gulp-nodemon]


### 生成api文档[参考][1]

* `npm i apidoc -g      =全局安装`
* `apidoc -i routes/ -o public/apidoc/      =生成api文档`
* `gulp server      =启动gulp服务(热更新服务)` 

### 其他知识
* [使用cheerio爬取网页数据][2]
* [unicode转码][3]


[1]:https://www.jianshu.com/p/7e1b057b047c/
[2]:https://www.cnblogs.com/CraryPrimitiveMan/p/3674421.html
[3]:http://tool.chinaz.com/tools/unicode.aspx
