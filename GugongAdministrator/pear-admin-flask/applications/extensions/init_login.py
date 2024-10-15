from flask_login import LoginManager


# 初始化登录管理器
def init_login_manager(app):
    # 创建登录管理器
    login_manager = LoginManager()
    # 初始化登录管理器
    login_manager.init_app(app)

    # 设置登录视图
    login_manager.login_view = 'system.passport.login'

    # 加载用户
    @login_manager.user_loader
    def load_user(user_id):
        # 从models中导入User模型
        from applications.models import User
        # 根据用户id查询用户
        user = User.query.get(int(user_id))
        # 返回用户
        return user
