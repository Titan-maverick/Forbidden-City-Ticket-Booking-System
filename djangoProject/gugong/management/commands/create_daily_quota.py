from django.core.management.base import BaseCommand
from django.utils import timezone
from gugong.models import DailyTicketQuota

class Command(BaseCommand):
    help = 'Create daily ticket quota if not exists'

    def add_arguments(self, parser):
        parser.add_argument('--date', type=str, help='指定日期 (YYYY-MM-DD)', required=True)
        parser.add_argument('--quantities', type=int, nargs=8, help='各类型可用余票数量，顺序为 [故宫上午, 故宫下午, 珍宝馆上午, 珍宝馆下午, 钟表馆上午, 钟表馆下午, 展览上午, 展览下午]', required=True)

    def handle(self, *args, **kwargs):
        date_str = kwargs['date']
        date = timezone.datetime.strptime(date_str, '%Y-%m-%d').date()  # 转换为日期对象
        quantities = kwargs['quantities']  # 获取各类型的可用余票数量

        if DailyTicketQuota.objects.filter(date=date).exists():
            self.stdout.write(self.style.WARNING('指定日期的票量记录已存在，不会创建新记录。'))
            return

        ticket_types = {
            1: '故宫',
            2: '珍宝馆',
            3: '钟表馆',
            4: '展览',
        }

        daily_quota_list = [
            DailyTicketQuota(
                museum_ticket_type=ticket_types[i],
                date=date,
                available_tickets=quantities[(i-1) * 2],  # 上午票
                select_time='上午'
            ) for i in range(1, 5)
        ] + [
            DailyTicketQuota(
                museum_ticket_type=ticket_types[i],
                date=date,
                available_tickets=quantities[(i-1) * 2 + 1],  # 下午票
                select_time='下午'
            ) for i in range(1, 5)
        ]

        DailyTicketQuota.objects.bulk_create(daily_quota_list)
        self.stdout.write(self.style.SUCCESS('成功创建每日票量记录'))
