# 【固定，不用动】app启动类
from django.apps import AppConfig


class GugongConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "gugong"

    def ready(self):
        import gugong.signals  # 导入信号