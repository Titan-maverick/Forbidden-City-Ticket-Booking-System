from django.core.management.base import BaseCommand
from django.db import transaction
from gugong.models import Order, OrderDetail, DailyTicketQuota, DailyTicketSale, TicketType, TicketSalesData

from decimal import Decimal
from datetime import datetime

class Command(BaseCommand):
    help = 'Refunds a ticket based on order ID'

    def add_arguments(self, parser):
        # 添加命令行参数，例如订单 ID
        parser.add_argument('order_id', type=str, help='The ID of the order to refund')

    @transaction.atomic
    def handle(self, *args, **kwargs):
        order_id = kwargs['order_id']
        try:
            self.refund_order_by_order_id(order_id)
            self.stdout.write(self.style.SUCCESS(f'Successfully refunded order: {order_id}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error refunding order {order_id}: {str(e)}'))

    def refund_order_by_order_id(self, order_id):
        # 在这里实现退票逻辑
        try:
            order = Order.objects.get(order_id=order_id)
            if(order.status == '已取消'):
                raise Exception("该订单已被取消，无法退票")
            # 获取该订单的详细信息
            order_details = OrderDetail.objects.filter(order=order).all()  # 根据订单查找对应的 OrderDetail 记录
            selected_date = order.order_date  # 获取订单日期
            selected_time = order.select_time  # 获取订单时间

            print(f"开始退票操作，订单号：{order_id}")
            print(f"订单日期: {selected_date}, 时间: {selected_time}")

            # 初始化观众列表
            audience_list = []
            for i in range(order.quantity):
                detail = order_details[0]  # 获取当前 OrderDetail 对象
                audience = {
                    'name': getattr(detail, f'name_{i + 1}'),  # 获取姓名，默认为 None
                    'ticket_type_id': getattr(detail, f'audience_ticket_type_id_{i + 1}_id'),
                    'isTreasureIslandSelected': getattr(detail, f'is_treasure_island_selected_{i + 1}'),
                    'isClockMuseumSelected': getattr(detail, f'is_clock_museum_selected_{i + 1}'),
                    'isExhibitionSelected': getattr(detail, f'is_exhibition_selected_{i + 1}'),
                }
                audience_list.append(audience)  # 将每个观众的信息添加到列表中

            total_price = 0
            for audience in audience_list:
                ticket_id = audience.get('ticket_type_id')
                isTreasureIslandSelected = audience.get('isTreasureIslandSelected')
                isClockMuseumSelected = audience.get('isClockMuseumSelected')
                isExhibitionSelected = audience.get('isExhibitionSelected')
                ticket_type = TicketType.objects.get(ticket_type_id=ticket_id)
                total_price += Decimal(ticket_type.price)
                if isTreasureIslandSelected:
                    ticket_type = TicketType.objects.get(ticket_type_id=ticket_id + 4)
                    total_price += Decimal(ticket_type.price)
                if isClockMuseumSelected:
                    ticket_type = TicketType.objects.get(ticket_type_id=ticket_id + 8)
                    total_price += Decimal(ticket_type.price)
                if isExhibitionSelected:
                    ticket_type = TicketType.objects.get(ticket_type_id=13)
                    total_price += Decimal(ticket_type.price)

            try:
                # 解析字符串为日期对象
                date_obj = datetime.strptime(selected_date, "%Y年%m月%d日")
                formatted_date = date_obj.strftime("%Y-%m-%d")  # 格式化为 YYYY-MM-DD
                # 更新售票数据
                sales_data = TicketSalesData.objects.get(
                    sale_date=formatted_date,
                    select_time=selected_time,
                )
                quota = DailyTicketQuota.objects.get(museum_ticket_type='故宫', date=formatted_date,
                                                     select_time=selected_time)
                quota_treasure = DailyTicketQuota.objects.get(museum_ticket_type='珍宝馆', date=formatted_date,
                                                              select_time=selected_time)
                quota_clock = DailyTicketQuota.objects.get(museum_ticket_type='钟表馆', date=formatted_date,
                                                           select_time=selected_time)
                quot_exhibition = DailyTicketQuota.objects.get(museum_ticket_type='展览', date=formatted_date,
                                                               select_time=selected_time)
                tickets_available = True

                # 用于更新每日销量(DailyTicketSale)
                daily_sales = {}  # 用于跟踪每日销量
                try:
                    with transaction.atomic():
                        for i in range(13):
                            ticket_type_ticket_id = TicketType.objects.get(ticket_type_id=i + 1)
                            daily_sales[i + 1], created = DailyTicketSale.objects.get_or_create(
                                ticket_type=ticket_type_ticket_id,
                                date=formatted_date,
                                select_time=selected_time,
                            )
                            ticket_type = TicketType.objects.get(ticket_type_id=i + 1)
                            daily_sales[i + 1].type_name = ticket_type.type_name
                        # 保存所有更新后的 daily_sales
                        for daily_sale in daily_sales.values():
                            daily_sale.save()
                except Exception as e:
                    print(f"Error occurred, rolling back changes: {e}")

                try:
                    with transaction.atomic():
                        # 更新每日票量(DailyTicketQuota)
                        for audience in audience_list:
                            quota.available_tickets += 1

                            ticket_id = audience.get('ticket_type_id')
                            isTreasureIslandSelected = audience.get('isTreasureIslandSelected')
                            isClockMuseumSelected = audience.get('isClockMuseumSelected')
                            isExhibitionSelected = audience.get('isExhibitionSelected')

                            # 根据票种更新售票数据(TicketSalesData)和每日销量(DailyTicketSale)
                            if tickets_available:
                                sales_data.gugong_ticket_count -= 1
                                # 更新每日销量
                                ticket_type_ticket_id = TicketType.objects.get(ticket_type_id=ticket_id)
                                daily_sales[ticket_id], created = DailyTicketSale.objects.get_or_create(
                                    ticket_type=ticket_type_ticket_id,
                                    date=formatted_date,
                                    select_time=selected_time,
                                )
                                daily_sales[ticket_id].ticket_count -= 1
                                ticket_type = TicketType.objects.get(ticket_type_id=ticket_id)
                                daily_sales[ticket_id].type_name = ticket_type.type_name
                                daily_sales[ticket_id].total_amount = Decimal(
                                    daily_sales[ticket_id].total_amount) - Decimal(
                                    ticket_type.price)

                            if isTreasureIslandSelected:
                                quota_treasure.available_tickets += 1

                                sales_data.treasure_island_ticket_count -= 1

                                # 更新每日销量
                                ticket_type_ticket_id = TicketType.objects.get(ticket_type_id=(ticket_id + 4))
                                daily_sales[ticket_id + 4], created = DailyTicketSale.objects.get_or_create(
                                    ticket_type=ticket_type_ticket_id,
                                    date=formatted_date,
                                    select_time=selected_time,
                                )
                                daily_sales[ticket_id + 4].ticket_count -= 1
                                ticket_type = TicketType.objects.get(ticket_type_id=(ticket_id + 4))
                                daily_sales[ticket_id + 4].type_name = ticket_type.type_name
                                daily_sales[ticket_id + 4].total_amount = Decimal(
                                    daily_sales[ticket_id + 4].total_amount) - Decimal(
                                    ticket_type.price)

                            if isClockMuseumSelected:
                                quota_clock.available_tickets += 1
                                sales_data.clock_museum_ticket_count -= 1
                                # 更新每日销量
                                ticket_type_ticket_id = TicketType.objects.get(ticket_type_id=(ticket_id + 8))
                                daily_sales[ticket_id + 8], created = DailyTicketSale.objects.get_or_create(
                                    ticket_type=ticket_type_ticket_id,
                                    date=formatted_date,
                                    select_time=selected_time,
                                )
                                daily_sales[ticket_id + 8].ticket_count -= 1
                                ticket_type = TicketType.objects.get(ticket_type_id=(ticket_id + 8))
                                daily_sales[ticket_id + 8].type_name = ticket_type.type_name
                                daily_sales[ticket_id + 8].total_amount = Decimal(
                                    daily_sales[ticket_id + 8].total_amount) - Decimal(
                                    ticket_type.price)

                            if isExhibitionSelected:
                                quot_exhibition.available_tickets += 1
                                sales_data.exhibition_ticket_count -= 1
                                # 更新每日销量
                                ticket_type_ticket_id = TicketType.objects.get(ticket_type_id=13)
                                daily_sales[13], created = DailyTicketSale.objects.get_or_create(
                                    ticket_type=ticket_type_ticket_id,
                                    date=formatted_date,
                                    select_time=selected_time,
                                )
                                daily_sales[13].ticket_count -= 1
                                ticket_type = TicketType.objects.get(ticket_type_id=13)
                                daily_sales[13].type_name = ticket_type.type_name
                                daily_sales[13].total_amount = Decimal(daily_sales[13].total_amount) - Decimal(
                                    ticket_type.price)
                            # 保存所有更新后的 daily_sales
                            for daily_sale in daily_sales.values():
                                daily_sale.save()

                        sales_data.amount -= Decimal(total_price)  # 假设每种票的价格相同，计算金额

                        # 仅在所有观众处理完且票仍可用时保存
                        if tickets_available:
                            quota.save()
                            quota_treasure.save()
                            quota_clock.save()
                            quot_exhibition.save()
                            sales_data.save()
                        else:
                            print('error:  退票失败')  # 确认更新
                except Exception as e:
                    print(f"Error occurred, rolling back changes: {e}")

            except Exception as e:
                print(f"Error in refunding tickets for order {order.order_id}: {e}")

        except Order.DoesNotExist:
            raise ValueError("Order not found.")

        order.status = '已取消'  # 更新订单状态为“已取消”
        order.save()  # 保存订单状态
        print(f'Order {order.order_id} status updated to 已取消')  # 确认更新

