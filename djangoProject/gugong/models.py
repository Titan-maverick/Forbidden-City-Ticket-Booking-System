# 【**重要**】，对数据库操作。
from django.db import models


# 用户模块
class User(models.Model):
    user_id = models.CharField(max_length=128, primary_key=True)  # 设置最大长度为 128，或其他合适的值
    phone_number = models.CharField(max_length=15, null=True, blank=True)  # 电话号码)
    registration_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Users'


class FrequentVisitor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='frequent_visitors')
    name_1 = models.CharField(max_length=20, blank=True, null=True)
    id_card_1 = models.CharField(max_length=50, blank=True, null=True)
    id_type_1 = models.IntegerField(choices=[
        (0, '身份证'),
        (1, '港澳居民往来内地通行证'),
        (2, '外国人永久居留身份证'),
        (3, '护照'),
        (4, '台湾居民来往大陆通行证'),
        (5, '港澳居民居住证'),
    ], default=0)  # 默认选择身份证类型

    name_2 = models.CharField(max_length=20, blank=True, null=True)
    id_card_2 = models.CharField(max_length=50, blank=True, null=True)
    id_type_2 = models.IntegerField(choices=[
        (0, '身份证'),
        (1, '港澳居民往来内地通行证'),
        (2, '外国人永久居留身份证'),
        (3, '护照'),
        (4, '台湾居民来往大陆通行证'),
        (5, '港澳居民居住证'),
    ], default=0)  # 默认选择身份证类型
    name_3 = models.CharField(max_length=20, blank=True, null=True)
    id_card_3 = models.CharField(max_length=50, blank=True, null=True)
    id_type_3 = models.IntegerField(choices=[
        (0, '身份证'),
        (1, '港澳居民往来内地通行证'),
        (2, '外国人永久居留身份证'),
        (3, '护照'),
        (4, '台湾居民来往大陆通行证'),
        (5, '港澳居民居住证'),
    ], default=0)  # 默认选择身份证类型
    name_4 = models.CharField(max_length=20, blank=True, null=True)
    id_card_4 = models.CharField(max_length=50, blank=True, null=True)
    id_type_4 = models.IntegerField(choices=[
        (0, '身份证'),
        (1, '港澳居民往来内地通行证'),
        (2, '外国人永久居留身份证'),
        (3, '护照'),
        (4, '台湾居民来往大陆通行证'),
        (5, '港澳居民居住证'),
    ], default=0)  # 默认选择身份证类型
    name_5 = models.CharField(max_length=20, blank=True, null=True)
    id_card_5 = models.CharField(max_length=50, blank=True, null=True)
    id_type_5 = models.IntegerField(choices=[
        (0, '身份证'),
        (1, '港澳居民往来内地通行证'),
        (2, '外国人永久居留身份证'),
        (3, '护照'),
        (4, '台湾居民来往大陆通行证'),
        (5, '港澳居民居住证'),
    ], default=0)  # 默认选择身份证类型

    class Meta:
        db_table = 'FrequentVisitors'


# 购票系统模块
class TicketType(models.Model):
    ticket_type_id = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=30)
    description = models.CharField(max_length=1000)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'TicketTypes'


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)  # 订单ID
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')  # 用户ID
    phone_number = models.CharField(max_length=15, null=True, blank=True)  # 电话号码
    quantity = models.IntegerField(default=0)  # 购买数量
    status = models.CharField(max_length=20)  # 状态
    order_date = models.CharField(max_length=50, blank=True, null=True)
    select_time = models.CharField(max_length=10)

    class Meta:
        db_table = 'Orders'
    def __str__(self):
        return f"Order {self.order_id} - Status: {self.status}"


class OrderDetail(models.Model):
    order_detail_id = models.AutoField(primary_key=True)  # 订单详情ID
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    name_1 = models.CharField(max_length=20, blank=True, null=True)
    id_card_1 = models.CharField(max_length=50, blank=True, null=True)
    id_type_1 = models.IntegerField(choices=[
        (0, '身份证'),
        (1, '港澳居民往来内地通行证'),
        (2, '外国人永久居留身份证'),
        (3, '护照'),
        (4, '台湾居民来往大陆通行证'),
        (5, '港澳居民居住证'),
    ], default=0)  # 默认选择身份证类型
    audience_ticket_type_id_1 = models.ForeignKey(TicketType, on_delete=models.CASCADE,
                                                  related_name='ticket_type_1', default=1)  # 观众的门票类型ID
    is_treasure_island_selected_1 = models.BooleanField(default=False)
    is_exhibition_selected_1 = models.BooleanField(default=False)
    is_clock_museum_selected_1 = models.BooleanField(default=False)

    # 同样为其他观众信息添加相应的字段
    name_2 = models.CharField(max_length=20, blank=True, null=True)
    id_card_2 = models.CharField(max_length=50, blank=True, null=True)
    id_type_2 = models.IntegerField(choices=[
        (0, '身份证'),
        (1, '港澳居民往来内地通行证'),
        (2, '外国人永久居留身份证'),
        (3, '护照'),
        (4, '台湾居民来往大陆通行证'),
        (5, '港澳居民居住证'),
    ], default=0)  # 默认选择身份证类型
    audience_ticket_type_id_2 = models.ForeignKey(TicketType, on_delete=models.CASCADE,
                                                  related_name='ticket_type_2', default=1)  # 观众的门票类型ID
    is_treasure_island_selected_2 = models.BooleanField(default=False)
    is_exhibition_selected_2 = models.BooleanField(default=False)
    is_clock_museum_selected_2 = models.BooleanField(default=False)

    # 继续为name_3, name_4, name_5添加类似字段
    name_3 = models.CharField(max_length=20, blank=True, null=True)
    id_card_3 = models.CharField(max_length=50, blank=True, null=True)
    id_type_3 = models.IntegerField(choices=[
        (0, '身份证'),
        (1, '港澳居民往来内地通行证'),
        (2, '外国人永久居留身份证'),
        (3, '护照'),
        (4, '台湾居民来往大陆通行证'),
        (5, '港澳居民居住证'),
    ], default=0)
    audience_ticket_type_id_3 = models.ForeignKey(TicketType, on_delete=models.CASCADE,
                                                  related_name='ticket_type_3', default=1)
    is_treasure_island_selected_3 = models.BooleanField(default=False)
    is_exhibition_selected_3 = models.BooleanField(default=False)
    is_clock_museum_selected_3 = models.BooleanField(default=False)

    name_4 = models.CharField(max_length=20, blank=True, null=True)
    id_card_4 = models.CharField(max_length=50, blank=True, null=True)
    id_type_4 = models.IntegerField(choices=[
        (0, '身份证'),
        (1, '港澳居民往来内地通行证'),
        (2, '外国人永久居留身份证'),
        (3, '护照'),
        (4, '台湾居民来往大陆通行证'),
        (5, '港澳居民居住证'),
    ], default=0)
    audience_ticket_type_id_4 = models.ForeignKey(TicketType, on_delete=models.CASCADE,
                                                  related_name='ticket_type_4', default=1)
    is_treasure_island_selected_4 = models.BooleanField(default=False)
    is_exhibition_selected_4 = models.BooleanField(default=False)
    is_clock_museum_selected_4 = models.BooleanField(default=False)

    name_5 = models.CharField(max_length=20, blank=True, null=True)
    id_card_5 = models.CharField(max_length=50, blank=True, null=True)
    id_type_5 = models.IntegerField(choices=[
        (0, '身份证'),
        (1, '港澳居民往来内地通行证'),
        (2, '外国人永久居留身份证'),
        (3, '护照'),
        (4, '台湾居民来往大陆通行证'),
        (5, '港澳居民居住证'),
    ], default=0)
    audience_ticket_type_id_5 = models.ForeignKey(TicketType, on_delete=models.CASCADE,
                                                  related_name='ticket_type_5', default=1)
    is_treasure_island_selected_5 = models.BooleanField(default=False)
    is_exhibition_selected_5 = models.BooleanField(default=False)
    is_clock_museum_selected_5 = models.BooleanField(default=False)

    class Meta:
        db_table = 'OrderDetails'


class BookingRecord(models.Model):
    record_id = models.AutoField(primary_key=True)  # 订票记录ID
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    purchase_date = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'BookingRecords'


# 销售数据模块
class TicketSalesData(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # 销售总金额
    sale_date = models.DateField()  # 销售日期
    select_time = models.CharField(max_length=10)  # 选择时间（上午或下午）
    gugong_ticket_count = models.IntegerField(default=0)  # 故宫门票的数量
    treasure_island_ticket_count = models.IntegerField(default=0)  # 珍宝岛门票的数量
    clock_museum_ticket_count = models.IntegerField(default=0)  # 钟表馆门票的数量
    exhibition_ticket_count = models.IntegerField(default=0)  # 展览的数量

    class Meta:
        db_table = 'TicketSalesData'
        unique_together = ('sale_date', 'select_time')  # 确保同一天同一时间段唯一


class DailyTicketSale(models.Model):
    ticket_type = models.ForeignKey(TicketType, on_delete=models.CASCADE)  # 门票类型ID，关联TicketType模型
    type_name = models.CharField(max_length=30)  # 类型名称
    date = models.DateField()  # 售卖日期
    select_time = models.CharField(max_length=10)  # 选择时间（上午或下午）
    ticket_count = models.IntegerField(default=0)  # 售卖的数量
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # 售卖的金额

    class Meta:
        db_table = 'DailyTicketSale'
        unique_together = ('ticket_type_id', 'date', 'select_time')  # 确保同一天同一时间段唯一


# 每日余票更新模块
class DailyTicketQuota(models.Model):
    TICKET_TYPES = [
        ('故宫', '故宫'),
        ('珍宝馆', '珍宝馆'),
        ('钟表馆', '钟表馆'),
        ('展览', '展览'),
    ]

    TIME_CHOICES = [
        ('上午', '上午'),
        ('下午', '下午'),
    ]

    museum_ticket_type = models.CharField(max_length=30, choices=TICKET_TYPES)  # 类型名称
    date = models.DateField()  # 日期
    available_tickets = models.IntegerField(default=0)  # 可用余票数量
    select_time = models.CharField(max_length=10, choices=TIME_CHOICES)  # 上午或下午

    class Meta:
        db_table = 'DailyTicketQuota'
        unique_together = ('date', 'museum_ticket_type', 'select_time')  # 唯一约束

    @classmethod
    def load_daily_quota(cls, specific_date, available_counts):
        for ticket_type in cls.TICKET_TYPES:
            for time in cls.TIME_CHOICES:
                cls.objects.update_or_create(
                    date=specific_date,
                    museum_ticket_type=ticket_type[0],
                    select_time=time[0],
                    defaults={'available_tickets': available_counts.get((ticket_type[0], time[0]), 0)},
                )
