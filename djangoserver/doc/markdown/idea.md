# 使用IntelliJ IDEA开发工具编写Web项目并部署服务器

### 一、使用Idea编写Web项目

项目地址：[**Github地址**][1]

![](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/08a84b99b5c94d53a9f962d8b259ada4~tplv-k3u1fbpfcp-zoom-1.image)

### 二、使用Idea部署Web项目

#### 1.使用Idea连接云服务器
> 依次选择`Tools`->`Deployment`->`Configuration`

在弹窗中输入`Host`、`User name`、`Password`连接云服务器

<div style="text-align: center;display: flex;flex-direction: row;">
<img style="width: 300px" src="https://p6-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/cad6b41fea004fbba342750ef95c5d13~tplv-k3u1fbpfcp-zoom-1.image"/>
  <div style="width:5px"></div>
  <img style="width: 300px;height:300px" src="https://p1-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/7b308daa6fb2484d95dd0f4d00cdd6ce~tplv-k3u1fbpfcp-zoom-1.image"/>
</div>

#### 2.使用Idea的`Terminal命令窗口`连接云服务器
> 依次选择`Tools`->`Start SSH session`打开连接云服务器的命令窗口

<div style="text-align: center">
<img style="width: 300px" src="https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/2aec4135245a495bbaa3d292eff366d5~tplv-k3u1fbpfcp-zoom-1.image">
  <div style="width:5px"></div>
<img style="width: 500px;" src="https://p1-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/b0f06d1c14bd49558e0a3bb725f27c6f~tplv-k3u1fbpfcp-zoom-1.image">
</div>

#### 3.在命令窗口执行`shell`命令来更新Web项目代码并启动服务

`uwsgi.sh`文件内容参考另一篇文章 [**使用uwsgi管理django服务**][2]

##### `uwsgi.sh`文件的核心代码
* 跳转到 djangoserver 目录下，更新代码
    > `cd $Django_path` `git pull`
* 使用`uwsgi`启动`django`服务
    > `uwsgi --ini uwsgi/uwsgi.ini`

**执行 `sh uwsgi.sh start` 命令即可启动`Django`服务**

![](https://p6-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/aba96ab7e0164d48976184b6472920d2~tplv-k3u1fbpfcp-zoom-1.image)

至此Django服务已经启动
---
----

### 三、Idea连接服务器后续

#### 1.Idea操作服务器文件或目录

使用上面的连接服务器操作后。
> 依次选择`Tools`->`Deployment`->`Browse Remote Host`

在Idea右侧出现的`Remote Host`窗口中就可以操作云服务器的文件目录。
支持的操作有`查看文件夹`、`查看、修改文件内容`、`新建、删除文件或文件夹`、`复制、剪切文件或文件夹`

<div style="text-align: center;display: flex;flex-direction: row;">
<img style="width: 300px;height:400px" src="https://p6-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/a54cbf4e97b141cea3eda98c751be89b~tplv-k3u1fbpfcp-zoom-1.image">
  <div style="width:5px"></div>
<img style="width: 300px" src="https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/147400ec8ede47a490bf046a8ce17cf1~tplv-k3u1fbpfcp-zoom-1.image">
</div>

#### 2.**Automatic Upload** 选项未测试
[Automatic Upload介绍][3]

因为腾讯云服务器的`Ftp`配置之后没有生效，一直有问题。

配置Ftp遇到的问题查看另一篇文章：[腾讯云服务器配置FTP][4]

所以不再研究这个了

[1]:https://github.com/yueyue10/ServerProject
[2]:https://juejin.im/post/6869581170578423822
[3]:https://www.cnblogs.com/jiguang/archive/2012/02/05/2339305.html
[4]:https://juejin.im/post/6858177266812354573
