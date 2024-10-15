# 项目名称
<div align="center">
<br/>
<br/>
  <h1 align="center">
    Forbidden City Ticket Booking System
  </h1>
  <h4 align="center">
    完全仿制故宫博物馆微信小程序的订票系统
  </h4> 
</div>

<div align="center">
  <img  width="92%" style="border-radius:10px;margin-top:20px;margin-bottom:20px;box-shadow: 2px 0 6px gray;" src="https://images.gitee.com/uploads/images/2020/1019/104805_042b888c_4835367.png" />
</div>

**请您点个 Star 多谢！🎉**
## 项目背景

这是大三数据库设计大作业的项目，旨在通过设计一个完整的数据库系统来提升我们的数据库理论与实践能力。
## 项目介绍
该项目旨在实现一个前后端分离、用于管理故宫博物馆门票的系统和一个管理员后台系统。用户可以对该系统进行个人信息填写、常用观众信息填写、门票查询、购买和查看订单记录等操作。管理员可以通过根据多种选项查询游客信息、查询每日、月、年的售票数据、统计营业数据、插入每天每种门票的数据。
## 技术结构
- **前端**：使用微信小程序开发工具进行开发。
- **后端**：使用Django, Flask行开发。
- **数据库**：使用MySQL进行数据存储。
## 业务结构
- **用户模块**：用户注册、登录、信息管理。
- **门票管理模块**：门票的查询、购买、管理。
- **数据统计模块**：数据的统计分析，提供决策支持。

## 业务流程
#### 用户:
1. 用户点击个人界面的登录按钮, 自动注册并登录系统。
2. 用户从首页的购票按钮进行浏览可用的门票信息。
3. 用户选择门票并进行购买。
4. 系统生成订单, 用户可以在订单界面进行查看订单详情功能。
#### 管理员:
1. 从后台找到对应的界面,进行查找和修改
## 项目展示
![项目展示图片](链接到项目展示的图片)

####  整个项目结构

```
该项目
├─GugongAdministrator/pear-admin-flask  # 管理员前后端的实现 来源于https://github.com/pearadmin/pear-admin-flask
│
├─MySQL_database  # 数据库测试与visio图
│
├─djangoProject  # 订票系统后端（Django）
│  
└─数据库课程设计  # 微信小程序前端 (微信小程序开发工具)

```
####  GugongAdministrator/pear-admin-flask项目结构

```
GugongAdministrator/pear-admin-flask
├─applications  # 应用
│  ├─common # 配置文件
│  │   └─script
│  │       └─admin.py  # 请在这里配置好默认管理员、页面调度
│  ├─extensions  # 注册插件
│  └─models  # 数据模型(只标注了拓展部分)
│      └─gugong.py  # 故宫数据库结构,方便其他文件调用
│  ├─views  # 视图部分(只标注了拓展部分)
│  │   ├─plugin 
│  │   └─system
│  │       ├─insert_ticket_data.py  # 插入、新建余票界面后端逻辑
│  │       ├─query_sale_data.py  # 根据信息查询游客信息界面后端逻辑
│  │       ├─query_sale_detail.py  # 售票数据(微观)后端逻辑
│  │       └─query_tourist.py  # 售票数据查询(宏观)后端逻辑
│  └─ config.py  # 配置文件对象, 请在这里配置好您的数据库、密钥
├─docs  # 文档说明（占坑）
├─migrations  # 迁移文件记录
├─plugins  # 
├─static  # 静态资源文件
├─templates  # 静态模板文件
│  ├error  # 报错页面
│  └─system  # 正常的页面(只标注了拓展部分)
│      ├─insert_ticket_data  # 插入,新建余票界面
│      ├─query_information  # 根据信息查询游客信息界面
│      ├─query_sale_data  # 售票数据查询(宏观)
│      └─query_sale_detail  # 售票数据(微观) 
├─app.py  # 应用程序的入口点
├─MySQL_connect_test.py  # 数据库连接测试
├─requirement.txt  # 依赖文件
└─test.py # 测试文件夹（测试一段字符对应的哈希密码）
```
####  内置功能

- [x] 用户管理：用户是系统操作者，该功能主要完成系统用户配置。
- [x] 权限管理：配置系统菜单，操作权限，按钮权限标识等。
- [x] 角色管理：角色菜单权限分配。
- [x] 操作日志：系统正常操作日志记录和查询；系统异常信息日志记录和查询。
- [x] 登录日志：系统登录日志记录查询包含登录异常。
- [x] 文件上传:   图片上传示例
- [x] 定时任务:   简单的定时任务
- [x] 管理员操作:   

####  djangoProject项目结构
```
djangoProject
├─djangoProject
│  ├─settings.py  # 请在这里配置您的项目
│  └─ urls.py  # 页面路由设置
├─gugong  # 文档说明（占坑）
│  ├─management  #
│  │   └─ commands
│  │         ├─create_daily_quota.py
│  │         ├─load_ticket_types.py
│  │         ├─refund_order.py
│  │         ├─update_daily_quota.py
│  │         └─update_order_status.py
│  ├─migrations  # 迁移文件记录
│  ├─apps.py  # app启动类
│  ├─models.py  # 对数据库操作
│  ├─signals.py  # 让信号在所有模型迁移完成后触发
│  ├─tasks.py  # 自定义任务(半小时支付检测)
│  └─views.py  # 处理用户请求并返回响应的核心文件
└─manage.py # 项目的命令行工具
```
####  内置功能
- [x] 微信登录：获取openid,并创建空表
- [x] 更新电话号码
- [x] 更新常用观众信息
- [x] 删除常用观众信息
- [x] 添加访客信息
- [x] 创建订单信息
- [x] 用户确认订单
- [x] 退票
- [x] 获取可用余票 
- [x] 获取其他可用余票

####  数据库课程设计项目结构
```
数据库课程设计
├─miniprogram  # 应用
│  ├─assets  # 配置文件
│  │  └─ images  # 图片文件
│  ├─miniprogram_npm  # 导入的库
│  ├─pages  # 数据模型
│  │  ├─choose_two_pavilion  # (购票)选择两馆
│  │  ├─confirm  # (购票)确认订单
│  │  ├─home  # 主页
│  │  ├─my  # 个人界面
│  │  ├─notice_page1  # (轮播图)对应页面
│  │  ├─notice_page2  # (轮播图)对应页面
│  │  ├─orders  # 订单记录
│  │  ├─pay  # (购票)支付
│  │  ├─ticket  # (购票)选择日期和票种
│  │  └─write_info  # (购票)填写个人信息
│  ├─stores  # 存储信息的文件
│  ├─app.js  # 小程序的主 JavaScript 文件
│  ├─app.json  # 小程序的全局配置文件
│  ├─app.wxss  # 小程序的全局样式表文件
│  ├─project.config.json  # 项目的配置信息
│  ├─project.private.config.json  # 存储敏感信息或开发环境的设置
│  └─sitemap.json  # 用于配置小程序的页面爬虫
└─其余文件  # 因为该项目是由另一个项目修改而来,可能会有一些多余的文件
```
####  内置功能

- [x] 参考故宫微信小程序的操作
- [x] 电话信息：个人开发者无法调用getphonenumber接口,只能手动输入。


## 项目配置？
```

#### 修改配置

```python
.env
# MySql配置信息
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_DATABASE=PearAdminFlask
MYSQL_USERNAME=root
MYSQL_PASSWORD=root

# Redis 配置
REDIS_HOST=127.0.0.1
REDIS_PORT=6379

# 密钥配置
SECRET_KEY='pear-admin-flask'

# 邮箱配置
MAIL_SERVER='smtp.qq.com'
MAIL_USERNAME='123@qq.com'
MAIL_PASSWORD='XXXXX' # 生成的授权码
```

## 如何快速上手这个项目？
- 请参考下方的启动指南:
#### 项目安装

# 安 装
pip install -r requirement\requirement-dev.txt

# 配 置
.env



#### Venv 安装

```bash
python -m venv venv
```

### 如何启动项目


#### 运行项目

```bash

flask init
```



#### 预览项目
