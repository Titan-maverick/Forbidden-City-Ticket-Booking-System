from django.core.management.base import BaseCommand
from gugong.models import Order


class Command(BaseCommand):
    help = '将指定订单的状态设置为已核销'

    def add_arguments(self, parser):
        parser.add_argument('--order_id', type=int, help='要更新状态的订单ID')

    def handle(self, *args, **kwargs):
        order_id = kwargs['order_id']

        if not order_id:
            self.stdout.write(self.style.ERROR('请提供有效的订单ID。'))
            return

        # 更新订单状态
        updated_count = Order.objects.filter(order_id=order_id).update(status='已核销')

        if updated_count > 0:
            self.stdout.write(self.style.SUCCESS(f'订单 {order_id} 的状态已成功更新为“已核销”。'))
        else:
            self.stdout.write(self.style.ERROR(f'未找到订单 {order_id}。'))
