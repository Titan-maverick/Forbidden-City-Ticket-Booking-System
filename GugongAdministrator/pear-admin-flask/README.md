#### 项目简介

Pear Admin Flask 基于 Flask 的后台管理系统，拥抱应用广泛的python语言，通过使用本系统，即可快速构建你的功能业务
项目旨在为 python 开发者提供一个后台管理系统的模板，可以快速构建信息管理系统。
项目使用flask-sqlalchemy + 权限验证 + marshmallow 序列化与数据验证

#### 内置功能

- [x] 用户管理：用户是系统操作者，该功能主要完成系统用户配置。
- [x] 权限管理：配置系统菜单，操作权限，按钮权限标识等。
- [x] 角色管理：角色菜单权限分配。
- [x] 操作日志：系统正常操作日志记录和查询；系统异常信息日志记录和查询。
- [x] 登录日志：系统登录日志记录查询包含登录异常。
- [x] 服务监控：监视当前系统CPU、内存、磁盘、python版本,运行时长等相关信息。
- [x] 文件上传:   图片上传示例


#### 项目结构

## 应用结构

```应用结构
Pear Admin Flask
├─applications  # 应用
│  ├─configs  # 配置文件
│  │  ├─ common.py  # 普通配置
│  │  └─ config.py  # 配置文件对象
│  ├─extensions  # 注册插件
│  ├─models  # 数据模型
│  ├─static  # 静态资源文件
│  ├─templates  # 静态模板文件
│  └─views  # 视图部分
│     ├─admin  # 后台管理视图模块
│     └─index  # 前台视图模块
├─docs  # 文档说明
├─migrations  # 迁移文件记录
├─requirement  # 依赖文件
└─.env # 项目的配置文件
```

## 资源结构

```资源结构
Pear Admin Flask
├─static    # 项目设定的 Flask 资源文件夹
│  ├─admin    # pear admin flask 的后端资源文件（与 pear admin layui 同步）
│  ├─index    # pear admin flask 的前端资源文件
│  └─upload     # 用户上传保存目录
└─templates # 项目设定的 Flask 模板文件夹
  ├─admin   # pear admin flask 的后端管理页面模板
  │  ├─admin_log    # 日志页面
  │  ├─common       # 基本模板页面（头部模板与页脚模板）
  │  ├─console      # 系统监控页面模板
  │  ├─dept         # 部门管理页面模板
  │  ├─dict         # 数据自动页面模板
  │  ├─mail         # 邮件管理页面模板
  │  ├─photo        # 图片上传页面模板
  │  ├─power        # 权限（菜单）管理页面模板
  │  ├─role         # 角色管理页面模板
  │  ├─task         # 任务设置页面模板
  │  └─user         # 用户管理页面模板
  ├─errors  # 错误页面模板
  └─index   # 主页模板
```

#### 项目安装

```bash
# 下 载
git clone https://gitee.com/pear-admin/pear-admin-flask
```

#### 修改配置

```python
# MySql配置信息
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_DATABASE=PearAdminFlask
MYSQL_USERNAME=root
MYSQL_PASSWORD=root

# 密钥配置
SECRET_KEY='一定要修改！！！'

# 邮箱配置
MAIL_SERVER='smtp.qq.com'
MAIL_USERNAME='123@qq.com'
MAIL_PASSWORD='XXXXX' # 生成的授权码
```

#### Venv 安装

```bash
python -m venv venv

# 进入虚拟环境下
pip install -r requirements.txt
```

#### 运行项目

```bash
# 初 始 化 数 据 库
flask db init
flask db migrate
flask db upgrade
flask admin init

# windows改为bat
./run.sh
```




#### 使用docker-compose运行项目

```bash
git clone https://gitee.com/pear-admin/pear-admin-flask

#安装docker-compose 
curl -L https://github.com/docker/compose/releases/download/1.26.2/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose 

#运行如下命令，有输入版本，表示docker-compose 可以用了
docker-compose --version 

#在当前目录执行如下命令即可以运行app
docker-compose -f dockercompose.yaml up

#看到如下表示运行成功，由于pip下载慢，需要一些时间，请耐心等待；如果安装失败，重新执行上面的命令即可。

#运行后在浏览器访问127.0.0.1：5000 

#如果要停止容器运行，在当前文件夹执行如下命令：
docker-compose -f dockercompose.yaml dwon


```

#### Pear Admin Flask 还有以下版本：


                    

**[mini 分支版本](https://gitee.com/pear-admin/pear-admin-flask/tree/mini/)**
不再更新

**[main 分支版本](https://gitee.com/pear-admin/pear-admin-flask/tree/main/)**
main 分支是对 mini 分支的后续，目前还在开发中。

#### 预览项目

|                        |                        |
| ---------------------- | ---------------------- |
| ![](docs/assets/1.jpg) | ![](docs/assets/2.jpg) |
| ![](docs/assets/3.jpg) | ![](docs/assets/4.jpg) |
| ![](docs/assets/5.jpg) | ![](docs/assets/6.jpg) |


