# MakeFriends
👥 A web site to make friends.

Welcome to following me. :)

<br>

## Architecture

### 前端技术栈：
Bootstrap 3 + FontAwesome + JavaScript + JQuery + MVT

### 后端技术栈：
Nginx反向代理 + uWSGI + Supervisor + MySQL + Redis + Django 1.11.1 + Python 3.6.5 + Celery异步任务

### 第三方服务：
七牛云对象存储

<br>

## Usage
`git clone`本项目至本地，依据`requirements.txt`创建虚拟环境；

在`settings`目录下创建`local_settings.py`添加`数据库配置`、`redis配置`、`七牛云access key`


<br>

## Updates:
* 2021-9-7: 文章详情页面包屑导航的添加

* 2021-9-6: 归档页面折叠栏

* 2021-8-23: 分页逻辑优化

* 2021-7-16: 评论系统由Disqus迁移到gitalk。

* 2021-7-15：基于echarts词云图重构便签云。增加链接到对应tag页面

* 2021-6-4: 模型展示（最近沉迷模型无法自拔）

* 2021-5: 页面icon更新 Bootstrap icon --> font-awesome icon

* ...中间更新未记录忘记了🤣

* 2020-4: 集成disqus，欢迎大家留言
