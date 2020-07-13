# Django框架介绍


### 一、常用命令

#### 1、创建一个django project
` django startproject mysite `
#### 2、在mysite目录下创建应用，比如blog:
` python manage.py startapp blog `
#### 3、启动django项目
`  python manage.py runserver 8080 `
#### 4、生成数据表
`准备：python manage.py makemigrations app`
`迁移：python manage.py migrate`
#### 5、创建超级用户
` python manage.py createsuperuser `
#### 6、Django 项目环境终端
`  python manage.py shell `
#### 7、Django 项目数据库环境终端
`  python manage.py dbshell `
#### 8、更多命令
`  python manage.py `
### 二、models知识


### 二、其他知识点
> URL传递参数
配置'^detail/(?P<article_id>[0-9]+)$'
'detail/<int:article_id>'

> 数据表删除后重新创建
>> delete from django_migrations where app='miniprogram';

### static配置

#### 3、STATIC文件还可以配置STATICFILES_DIRS，指定额外的静态文件存储位置。
    #  STATIC_URL的含义与MEDIA_URL类似。

    # ----------------------------------------------------------------------------
    #注意1:
        #为了后端的更改不会影响前端的引入，避免造成前端大量修改

        STATIC_URL = '/static/'               #引用名
        STATICFILES_DIRS = (
            os.path.join(BASE_DIR,"statics")  #实际名 ,即实际文件夹的名字
        )

        #django对引用名和实际名进行映射,引用时,只能按照引用名来,不能按实际名去找
        #<script src="/statics/jquery-3.1.1.js"></script>
        #------error－－－－－不能直接用，必须用STATIC_URL = '/static/':
        #<script src="/static/jquery-3.1.1.js"></script>

    #注意2(statics文件夹写在不同的app下,静态文件的调用):

        STATIC_URL = '/static/'

        STATICFILES_DIRS=(
            ('hello',os.path.join(BASE_DIR,"app01","statics")) ,
        )

        #<script src="/static/hello/jquery-1.8.2.min.js"></script>

    #注意3:
        STATIC_URL = '/static/'
        {% load staticfiles %}
       # <script src={% static "jquery-1.8.2.min.js" %}></script>
`



[1]:https://blog.csdn.net/hanglinux/article/details/75645756
