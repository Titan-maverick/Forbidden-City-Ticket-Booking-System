from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote as urlquote

# 创建 Flask 应用
app = Flask(__name__)

# 数据库配置
MYSQL_USERNAME = 'root'
MYSQL_PASSWORD = 'niuzeyu123'
MYSQL_HOST = 'localhost'
MYSQL_PORT = 3306
MYSQL_DATABASE = 'museum'

app.config['SQLALCHEMY_BINDS'] = {
    'museum_db': f"mysql+pymysql://{MYSQL_USERNAME}:{urlquote(MYSQL_PASSWORD)}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}?charset=utf8mb4"
}

# 初始化 SQLAlchemy
db = SQLAlchemy(app)


# 用户模块
class User(db.Model):
    __tablename__ = 'Users'
    __bind_key__ = 'museum_db'
    user_id = db.Column(db.String(128), primary_key=True)
    phone_number = db.Column(db.String(15), nullable=True)
    registration_date = db.Column(db.DateTime, server_default=db.func.now())


# 测试数据库连接
@app.route('/test_museum_db')
def test_museum_db():
    try:
        users = User.query.all()  # 直接使用 User.query
        return f"Connected to museum_db successfully! Found {len(users)} users."
    except Exception as e:
        return f"Error connecting to museum_db: {str(e)}"

# 启动应用
if __name__ == '__main__':
    app.run(debug=True)
