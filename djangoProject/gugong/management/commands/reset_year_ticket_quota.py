from django.core.management.base import BaseCommand
from gugong.models import YearTicketQuota

class Command(BaseCommand):
    help = 'Reset available tickets for all users to zero'

    def handle(self, *args, **kwargs):
        # 获取所有 YearTicketQuota 记录
        year_ticket_quotas = YearTicketQuota.objects.all()

        if not year_ticket_quotas.exists():
            self.stdout.write(self.style.WARNING('没有找到任何年票配额记录。'))
            return

        # 将所有用户的 available_tickets 设为 0
        updated_count = year_ticket_quotas.update(available_tickets=0)

        self.stdout.write(self.style.SUCCESS(f'成功将 {updated_count} 个用户的年票余额清零。'))