from django.core.management.base import BaseCommand
from django.utils import timezone
from gugong.models import DailyTicketQuota

class Command(BaseCommand):
    help = 'Update available tickets for a specific ticket type and time'

    def add_arguments(self, parser):
        parser.add_argument('--date', type=str, help='指定日期 (YYYY-MM-DD)', required=True)
        parser.add_argument('--ticket_type', type=str, help='票种 (故宫, 珍宝馆, 钟表馆, 展览)', required=True)
        parser.add_argument('--select_time', type=str, help='选择时间 (上午, 下午)', required=True)
        parser.add_argument('--available_tickets', type=int, help='可用余票数量', required=True)

    def handle(self, *args, **kwargs):
        date_str = kwargs['date']
        date = timezone.datetime.strptime(date_str, '%Y-%m-%d').date()  # 转换为日期对象
        ticket_type = kwargs['ticket_type']
        select_time = kwargs['select_time']
        available_tickets = kwargs['available_tickets']

        # 更新可用余票数量
        quota, created = DailyTicketQuota.objects.update_or_create(
            date=date,
            museum_ticket_type=ticket_type,
            select_time=select_time,
            defaults={'available_tickets': available_tickets}
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f'成功创建 {date} 的 {ticket_type} {select_time} 可用余票数量为 {available_tickets}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'成功更新 {date} 的 {ticket_type} {select_time} 可用余票数量为 {available_tickets}'))