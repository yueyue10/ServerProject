### 在Django项目的接口中使用Python实时爬虫的数据

项目中使用了豆瓣的开放接口，最近发现豆瓣电影接口不能用了，所以想着要自己动手做一个`爬取豆瓣电影数据`的接口。

![](https://p1-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/a5e2d2304f97487995d618a34e54288c~tplv-k3u1fbpfcp-zoom-1.image)

### 豆瓣热映电影

![](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/e6ed6b13e1174e25a6a53a125a3d7264~tplv-k3u1fbpfcp-zoom-1.image)

**开发后的接口地址**：https://zhaoyj.work/poetry/movie/showing

**返回内容如下：**
![](https://p9-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/692663bd16aa44a889a97a530af41519~tplv-k3u1fbpfcp-zoom-1.image)

### 一、创建`Django`服务项目

[**Django项目地址**][1]

![](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/8f7713e07a15493c8a25831a3b65730a~tplv-k3u1fbpfcp-zoom-1.image)

### 二、在项目的应用目录`miniprogram`下创建`spiderHot.py`爬虫程序

#### 1.在`spiderHot.py`中创建`MovieBean`电影实体类
![](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/214b8106d5df4f60a05f02cc03f1efc7~tplv-k3u1fbpfcp-zoom-1.image)

#### 2.在`spiderHot.py`中创建`HotMovieSpider`爬取热映电影类
* 1.编写`get_html_text`方法，获取html页码内容
    ```
    def get_html_text(url, headers=None):
        time.sleep(random.uniform(0.5, 1.5))
        response = requests.get(url, headers=ComHeaders.pc_headers, timeout=(5, 60))
        html_text = ''
        if response.status_code == 200:
            html_text = response.text
        return html_text
    ```
* 2.编写`get_info_from_movie`方法，获取电影数据
    > 通过`xpath`查找标签及文本内容，创建`MovieBean`对象添加到集合中并返回集合数据
    ```
    def get_info_from_movie(self, href):
        html_detail = self.get_html_text(href)
        com_html = etree.HTML(html_detail)
        movieLis = com_html.xpath('//*[@id="nowplaying"]/div[@class="mod-bd"]/ul/li')
        movieList = []
        for index, movieItem in enumerate(movieLis):
            if index == 6:
                break
            subject = movieItem.xpath('./@data-subject')[0]
            title = movieItem.xpath('./@data-title')[0]
            director = movieItem.xpath('./@data-director')[0]
            actor = movieItem.xpath('./@data-actors')[0]
            area = movieItem.xpath('./@data-region')[0]
            duration = movieItem.xpath('./@data-duration')[0]
            score = movieItem.xpath('./@data-score')[0]
            image = movieItem.xpath('./ul/li[@class="poster"]/a/img/@src')[0]
            movieBean = MovieBean(subject, title, image, score, director, actor, duration, area)
            movieList.append(movieBean)
        return movieList
    ```
* 3.编写`start`方法，启动爬虫程序并返回爬取数据
    > 将上面`get_info_from_movie`方法返回的电影集合数据转成json字符串<直接返回集合数据到接口中有问题>
    ```
    def start(self):
        movieList = self.get_info_from_movie(self.url)
        movieList_json = json.dumps(movieList, default=lambda obj: obj.__dict__, sort_keys=True, indent=4)
        return movieList_json
    ```
### 三、在项目的应用目录`miniprogram`下的`views`里面编写业务代码

#### 1.在`views`包下创建`movie.py`文件并编写业务方法`movie_hot`获取热映电影数据并返回
> 将`HotMovieSpider`程序中返回的json字符串转成`JSON数据`并返回
```
def movie_hot(request, format=None):
    spider = HotMovieSpider()
    movieList = spider.start()
    movieListJson = json.loads(movieList)
    return result.success(movieListJson)
```

#### 2.在`miniprogram`的`urls.py`中添加接口地址
```
path(r'movie/showing', movie.movie_hot),
```

### 四、部署Django项目后即可使用该接口


[1]:https://github.com/yueyue10/ServerProject/tree/master/djangoserver
