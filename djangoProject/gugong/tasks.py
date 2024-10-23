from datetime import datetime, timedelta
import pytz
from django.utils import timezone
from background_task import background
from .models import BookingRecord, Order, TicketSalesData, DailyTicketQuota, OrderDetail, TicketType, DailyTicketSale
from decimal import Decimal
from django.db import transaction
from django.core.management import call_command


@background(schedule=60)  # 每分钟执行一次任务
def check_and_cancel_unpaid_orders():
    # 定义北京时间时区
    beijing_tz = pytz.timezone('Asia/Shanghai')

    # 获取当前时间（带时区）
    now = timezone.now().astimezone(beijing_tz)

    # 获取超过30分钟的时间点（带时区）
    cutoff_time = now - timedelta(minutes=1)

    # 查找未支付的订单记录
    unpaid_records = BookingRecord.objects.all()

    # 用于存储符合条件的未支付订单
    unpaid_orders = []

    for record in unpaid_records:
        # 将 purchase_date 转换为 datetime 对象（并设置为北京时间）
        try:
            purchase_time = datetime.strptime(record.purchase_date, "%Y年%m月%d日%H:%M")
            purchase_time = beijing_tz.localize(purchase_time)  # 本地化为北京时间

            # 检查 purchase_time 是否超过30分钟
            if purchase_time <= cutoff_time:
                # 检查订单状态是否为“待支付”
                if record.order.status == '待支付':  # 确保订单状态为“待支付”
                    unpaid_orders.append(record.order)  # 记录对应的订单
        except ValueError:
            print(f"Error parsing date for record: {record.order_id}")
    # 更新未支付的订单状态
    for order in unpaid_orders:

        # 开始退票逻辑，恢复可用票量
        order_details = OrderDetail.objects.filter(order=order).all()  # 根据订单查找对应的 OrderDetail 记录
        selected_date = order.order_date  # 获取订单日期
        selected_time = order.select_time  # 获取订单时间

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
        # print(audience_list)
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

            # print('total_price', total_price)
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
                    print({'error': '退票失败'})
        except Exception as e:
            print(f"Error in refunding tickets for order {order.order_id}: {e}")

        order.status = '已取消'  # 更新订单状态为“已取消”
        order.save()  # 保存订单状态
        print(f'Order {order.order_id} status updated to 已取消')  # 确认更新


# 定时任务，每天零点执行，设置七天后的余票量
@background(schedule=24 * 60 * 60)  # 每24小时执行一次
def set_ticket_quota_for_seven_days_ahead():
    # 获取当前时间的北京时间，并计算七天后的日期
    beijing_tz = pytz.timezone('Asia/Shanghai')
    now = timezone.now().astimezone(beijing_tz)

    # 获取当前时间，并计算七天后的日期
    seven_days_ahead = now.date() + timedelta(days=7)

    # 自定义每种票量的默认余票
    default_quantities = [20, 20, 20, 20, 20, 20, 20, 20]  # 故宫、珍宝馆、钟表馆、展览上午和下午的票量

    # 调用 `create_ticket_quota` 命令来设置七天后的票量
    call_command('create_daily_quota', date=seven_days_ahead.strftime('%Y-%m-%d'), quantities=default_quantities)


# 在项目启动时，将任务设定为当天零点开始
def schedule_ticket_quota_task():
    beijing_tz = pytz.timezone('Asia/Shanghai')
    now = timezone.now().astimezone(beijing_tz)

    # 计算当天零点的时间
    midnight = datetime.combine(now.date(), datetime.min.time()).astimezone(beijing_tz)

    # 如果当前时间已经过了零点，任务应该从第二天零点开始
    if now > midnight:
        midnight += timedelta(days=1)

    # 调度任务在指定的零点时间执行
    set_ticket_quota_for_seven_days_ahead(schedule=midnight)
