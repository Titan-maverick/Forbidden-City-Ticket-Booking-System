from django.core.management.base import BaseCommand
from gugong.models import TicketType

class Command(BaseCommand):
    help = 'Load initial ticket types'

    def handle(self, *args, **kwargs):
        # 创建一个TicketType对象列表
        ticket_types = [
            TicketType(ticket_type_id=1, type_name='标准票', price=60, description=''),
            TicketType(ticket_type_id=2, type_name='老年人票', price=30, description=''),
            TicketType(ticket_type_id=3, type_name='未成年人免费票', price=0, description=''),
            TicketType(ticket_type_id=4, type_name='学生票', price=20, description=''),
            TicketType(ticket_type_id=5, type_name='珍宝馆标准票', price=10, description=''),
            TicketType(ticket_type_id=6, type_name='珍宝馆老年人票', price=5, description=''),
            TicketType(ticket_type_id=7, type_name='珍宝馆未成年人票', price=0, description=''),
            TicketType(ticket_type_id=8, type_name='珍宝馆学生票', price=5, description=''),
            TicketType(ticket_type_id=9, type_name='钟表馆标准票', price=10, description=''),
            TicketType(ticket_type_id=10, type_name='钟表馆老年人票', price=5, description=''),
            TicketType(ticket_type_id=11, type_name='钟表馆未成年人票', price=0, description=''),
            TicketType(ticket_type_id=12, type_name='钟表馆学生票', price=5, description=''),
            TicketType(ticket_type_id=13, type_name='展览', price=0, description='千秋佳人--故宫博物院藏历代人物画特展(第四期)'),
            TicketType(ticket_type_id=14, type_name='故宫年票', price=0, description=''),
        ]
        # 批量创建TicketType对象
        TicketType.objects.bulk_create(ticket_types)
        # 输出成功加载票种的消息
        self.stdout.write(self.style.SUCCESS('Successfully loaded ticket types'))