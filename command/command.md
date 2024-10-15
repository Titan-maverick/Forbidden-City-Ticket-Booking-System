### Django后端, 启动!
'''
cd "E:\Project\pycharm project\gugong_Django\djangoProject"

python manage.py runserver 8000
'''
### 将端口内网穿透到公网
ngrok config add-authtoken 您的密钥
ngrok http --domain=bass-epic-mentally.ngrok-free.app 8000  # 免费的

### 告诉 Django 你对模型所做的更改
python manage.py makemigrations 

### 将更改写入数据库
python manage.py migrate

### 设定TicketType
python manage.py load_ticket_types

### 设定指定日期的余票
python manage.py create_daily_quota --date 时间 --quantities (故宫上午) (故宫下午) (珍宝馆上午) (珍宝馆下午) (钟表馆上午) (钟表馆下午) (展览上午) (展览下午)
eg: 
python manage.py create_daily_quota --date 2024-10-01 --quantities 100 80 50 30 40 20 70 60

###  更新指定的余票
eg: 
python manage.py update_daily_quota --date 2024-10-01 --ticket_type "故宫" --select_time "上午" --available_tickets 100

### 更新指定订单的状态为已核销(验票)
python manage.py update_order_status --order_id 您要改变的订单号

### 自动取消超过半小时未支付的票
python manage.py process_tasks

###  退指定订单id的订单
python manage.py refund_order 订单号

### 为预订年票的用户填写年票余额
python manage.py set_year_ticket_quota --phone=<用户电话号码> --available_tickets=10

### 年底将所有年票清空
python manage.py reset_year_ticket_quota
