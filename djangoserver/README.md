# DjangoServer - django框架的服务
admin管理后台使用的是[simpleui][1]

项目部署地址：https://zhaoyj.work/poetry/docs/

### 一、项目创建

**1.初始化 `djangoserver` project**
>`django startproject djangoserver`

#### _下面的 `manage.py` 是经过上面的命令生成的项目管理程序_


**2.创建 `miniprogram` 应用**
>`python manage.py startapp miniprogram`


### 二、项目配置

#### 1.配置`djangoserver`目录下的`settings.py`
* 配置项目下的应用关联
    ```
    INSTALLED_APPS = [
        'simpleui',
        'miniprogram'
    ]
    ```
* 配置项目安全插件:[middleware][2]
    ```
    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware'
    ]
    ```
* 配置Admin后台中文
    ```
    LANGUAGE_CODE = 'zh-hans'
    ```
* 配置`rest-docs`
    ```
    INSTALLED_APPS = [
        'rest_framework',
        'rest_framework.authtoken'
    ]
    REST_FRAMEWORK = {
        'DEFAULT_PERMISSION_CLASSES': [
            'rest_framework.permissions.DjangoModelPermissions'
        ],
        'DEFAULT_AUTHENTICATION_CLASSES': (
        ),
        'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.AutoSchema',
    }
    ```


#### 2.Django服务部署后，Admin后台页面样式显示错乱

**1.配置服务器的nginx: 添加 `Django` 项目的 `static` 文件路径**
```
location /static/ {
   autoindex on;
   alias /data/project/ServerProject/djangoserver/collect_static/;
}
```
**2.在服务器使用Django的 `manage.py` 生成静态文件**

* 2.1 配置静态文件生成路径：
    在`djangoserver`目录的`settings.py`中配置
    ```
    STATIC_ROOT = os.path.join(BASE_DIR, 'collect_static')
    ```
* 2.2 在服务器中使用下面的代码生成项目的静态文件
    > `python3 manage.py collectstatic`


### 三、`miniprogram`应用业务处理
以下默认的文件路径都是`miniprogram`

#### 1.接口路径`url`配置
* 修改 `djangoserver` 下的 `urls.py`
    ```
    urlpatterns = [
        path('poetry/', include('miniprogram.urls')),
        url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
        url(r'docs/', include_docs_urls(title='接口文档', authentication_classes=[], permission_classes=[])),
    ]
    ```
* 在 `miniprogram` 下增加 `views` 包，将 `views.py` 移动到该包下并修改为 `index.py`
* 修改 `miniprogram` 下的 `urls.py`
    ```
    urlpatterns = [
        path('index/', index.index),
        ...
    ]
    ```

#### 2.在 `models.py` 中编写数据表对应的数据类
```
# 年级数据
class GradeType(models.Model):
    grade_name = models.CharField(max_length=15, )
    grade_image = models.URLField()
    poetry_flag = models.IntegerField(db_index=True)

    def __str__(self):
        return self.grade_name
```
#### 2.1 使用`manage.py`生成数据库的数据表
准备
> `python manage.py makemigrations`

迁移
> `python manage.py migrate`

#### 3.普通的`接口数据`返回
* 在 `djangoserver` 下增加 `result.py`
    ```
    class HttpCode(object):
        success = 0
        error = 1
    def result(code=HttpCode.success, message='', data=None, kwargs=None):
        json_dict = {'code': code, 'data': data, 'message': message}
        if kwargs and isinstance(kwargs, dict) and kwargs.keys():
            json_dict.update(kwargs)
        return JsonResponse(json_dict, json_dumps_params={'ensure_ascii': False})
    def success(data=None):
        return result(code=HttpCode.success, message='OK', data=data)
    def error(message='', data=None):
        return result(code=HttpCode.error, message=message, data=data)
    ```
* 在`views`包下的`python`文件中编写业务代码并返回接口数据
    ```
    def grade_types(request):
        queryset = models.GradeType.objects.all().values('grade_name', 'grade_image', 'poetry_flag')
        return result.success(list(queryset))
    ```
  
#### 4.使用`RestApi`形式的接口返回数据
这种方式的好处在于方便管理数据类返回的属性
* 添加`serializers.py`文件并编写`数据类`的`实例化类`
    ```
    class PoetrySerializer(serializers.ModelSerializer):
        class Meta:
            model = Poetry
            fields = ('title', 'time', 'author', 'content', 'pic')
    ```
* 在`views`下编写业务代码,省去了上面使用`values`的方法。
    ```
    @api_view(['GET'])
    def grade_list(request, format=None):
        """
        获取年级列表数据
        """
        grade_types = GradeType.objects.all()
        serializer = GradeTypeSerializer(grade_types, many=True)
        return Response(serializer.data)
    ```

#### 5.接口参数问题
* 第一种方式：在`urls.py`中配置`请求url`时，同时配置`请求参数`
    * 编写`urls.py`中的代码
        ```
        path(r'poetry/<int:poetry_flag>', index.poetry)
        ```
    * 编写`views`下的业务代码
        ```
        def poetry(request, poetry_flag):
            queryset = models.Poetry.objects.filter(poetry_flag=poetry_flag).values('title')
            return result.success(list(queryset))
        ```
* 第二种方式：直接在`views`下的业务代码中获取`请求参数`
    ```
    def poetry_rank(request):
        page_num = request.GET.get('pageNum')
    ```
* 在项目中使用`动态参数`来使用别的接口的方法
    ```
    def poetry_rank(request):
        page_num = request.GET.get('pageNum')
        page_index = request.GET.get('pageIndex')
        rankFlag = models.PoetryFlag.objects.get(poetry_type='诗词排行榜')
        return poetry_list(request, page_num=page_num, page_index=page_index, poetry_flag=rankFlag.poetry_flag)
    
    def poetry_list(request, **kw):
        if kw:
            page_num = kw['page_num']
            page_index = kw['page_index']
            poetry_flag = kw['poetry_flag']
        else:
            page_num = request.GET.get('pageNum')
            page_index = request.GET.get('pageIndex')
            poetry_flag = request.GET.get('poetry_flag')
        queryset = models.Poetry.objects.filter(poetry_flag=poetry_flag).order_by('mark_index').values('title')
        ...
    ```



### 四、Admin后台相关

> 配置后台管理数据表
* 修改 `miniprogram` 下的 `admin.py`中的代码
    ```
    admin.site.register(models.Poetry)
    ```
> 相关命令
* 创建超级用户用于登陆Admin后台
    > `python manage.py createsuperuser`

### 五、`REST-API`接口文档

虽然使用了这个文档，但这个文档也是很不友好的。不支持如`显示参数`等注解，页面显示的也不是很好。
最主要的是相关文档较少，使用比较费劲。

> 必须具备以下两个条件才能在`docs`接口文档下显示出来
* 添加`@api_view`注解
    ```
    @api_view(['GET'])
    ```
* 使用`数据类`的`实例化类`处理业务逻辑并返回数据  


### 六、项目部署
参考[将Django项目部署到服务器][3]

**项目使用`UWSGI`管理服务**

#### 1.创建`uwsgi`目录并在目录下编写`uwsgi`相关程序
* 编写`uwsgi.ini`文件
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
* 创建`uwsgi.pid`文件
* 创建`uwsgi.status`文件
#### 2.`uwsgi`相关命令
* 启动uwsgi服务
    > `uwsgi --ini uwsgi.ini`
* 重启uwsgi服务
    > `uwsgi --reload uwsgi/uwsgi.pid`
* 查看uwsgi状态
    > `uwsgi --connect-and-read uwsgi/uwsgi.status`
* 停止uwsgi服务
    > `uwsgi --stop uwsgi/uwsgi.pid`

#### 3.在服务器使用`doc/shell/uwsgi.sh`来启动和停止`django`服务



[1]:https://simpleui.88cto.com/simpleui/
[2]:https://blog.csdn.net/yyy72999/article/details/80324950
[3]:https://www.jianshu.com/p/36ef6557c910
