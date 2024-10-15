from django.core.management.base import BaseCommand
from gugong.models import YearTicketQuota, User

class Command(BaseCommand):
    help = 'Set available tickets for the specified user by phone number, or create one if it does not exist'

    def add_arguments(self, parser):
        parser.add_argument('--phone', type=str, help='用户的电话号码', required=True)
        parser.add_argument('--available_tickets', type=int, help='可用票数量', required=True)

    def handle(self, *args, **kwargs):
        phone = kwargs['phone']
        available_tickets = kwargs['available_tickets']

        # 根据电话号码查找用户
        try:
            user = User.objects.get(phone_number=phone)
            user_id = user.user_id
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('未找到该电话号码对应的用户。'))
            return

        # 查找用户的 YearTicketQuota
        year_ticket_quota, created = YearTicketQuota.objects.get_or_create(
            user_id=user_id,
            defaults={'available_tickets': available_tickets}
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f'成功创建年票配额记录，设置可用票数量为 {available_tickets}。'))
        else:
            # 如果记录已存在，则更新可用票数量
            year_ticket_quota.available_tickets = available_tickets
            year_ticket_quota.save()
            self.stdout.write(self.style.SUCCESS(f'成功将可用票数量更新为 {available_tickets}。'))