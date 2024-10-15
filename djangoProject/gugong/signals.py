from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .tasks import check_and_cancel_unpaid_orders

@receiver(post_migrate)  # 这个信号在所有模型迁移完成后触发
def start_background_tasks(sender, **kwargs):
    check_and_cancel_unpaid_orders(repeat=60)  # 启动任务
