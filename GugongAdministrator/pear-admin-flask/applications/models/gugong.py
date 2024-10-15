from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
db = SQLAlchemy()


# 用户模块
class User(db.Model):
    __tablename__ = 'Users'
    __bind_key__ = 'museum_db'
    user_id = db.Column(db.String(128), primary_key=True)
    phone_number = db.Column(db.String(15), nullable=True)
    registration_date = db.Column(db.DateTime)

    frequent_visitors = relationship('FrequentVisitor', back_populates='user')
    orders = relationship('Order', back_populates='user')
    booking_records = relationship('BookingRecord', back_populates='user')


class FrequentVisitor(db.Model):
    __tablename__ = 'FrequentVisitors'
    __bind_key__ = 'museum_db'
    id = db.Column(db.Integer, primary_key=True)  # 新增主键
    user_id = db.Column(db.String(128), ForeignKey('Users.user_id'))
    user = relationship('User', back_populates='frequent_visitors')

    name_1 = db.Column(db.String(20), nullable=True)
    id_card_1 = db.Column(db.String(50), nullable=True)
    id_type_1 = db.Column(db.Integer, default=0)  # 默认选择身份证类型

    name_2 = db.Column(db.String(20), nullable=True)
    id_card_2 = db.Column(db.String(50), nullable=True)
    id_type_2 = db.Column(db.Integer, default=0)

    name_3 = db.Column(db.String(20), nullable=True)
    id_card_3 = db.Column(db.String(50), nullable=True)
    id_type_3 = db.Column(db.Integer, default=0)

    name_4 = db.Column(db.String(20), nullable=True)
    id_card_4 = db.Column(db.String(50), nullable=True)
    id_type_4 = db.Column(db.Integer, default=0)

    name_5 = db.Column(db.String(20), nullable=True)
    id_card_5 = db.Column(db.String(50), nullable=True)
    id_type_5 = db.Column(db.Integer, default=0)


# 购票系统模块
class TicketType(db.Model):
    __tablename__ = 'TicketTypes'
    __bind_key__ = 'museum_db'
    ticket_type_id = db.Column(db.Integer, primary_key=True)  # 自增ID
    type_name = db.Column(db.String(30))
    description = db.Column(db.String(1000))
    price = db.Column(db.Numeric(10, 2))


class Order(db.Model):
    __tablename__ = 'Orders'
    __bind_key__ = 'museum_db'
    order_id = db.Column(db.Integer, primary_key=True)  # 订单ID
    user_id = db.Column(db.String(128), ForeignKey('Users.user_id'))
    user = relationship('User', back_populates='orders')
    phone_number = db.Column(db.String(15), nullable=True)
    quantity = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20))
    order_date = db.Column(db.String(50), nullable=True)
    select_time = db.Column(db.String(10))
    order_details = relationship('OrderDetail', back_populates='order')
    booking_records = relationship('BookingRecord', back_populates='order')

    def __repr__(self):
        return f"<Order {self.order_id} - Status: {self.status}>"


class OrderDetail(db.Model):
    __tablename__ = 'OrderDetails'
    __bind_key__ = 'museum_db'
    order_detail_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, ForeignKey('Orders.order_id'))
    order = relationship('Order', back_populates='order_details')

    name_1 = db.Column(db.String(20), nullable=True)
    id_card_1 = db.Column(db.String(50), nullable=True)
    id_type_1 = db.Column(db.Integer, default=0)
    audience_ticket_type_id_1_id = db.Column(db.Integer, ForeignKey('TicketTypes.ticket_type_id'), default=1)
    is_treasure_island_selected_1 = db.Column(db.Boolean, default=False)
    is_exhibition_selected_1 = db.Column(db.Boolean, default=False)
    is_clock_museum_selected_1 = db.Column(db.Boolean, default=False)

    # 继续为其他观众添加字段
    name_2 = db.Column(db.String(20), nullable=True)
    id_card_2 = db.Column(db.String(50), nullable=True)
    id_type_2 = db.Column(db.Integer, default=0)
    audience_ticket_type_id_2_id = db.Column(db.Integer, ForeignKey('TicketTypes.ticket_type_id'), default=1)
    is_treasure_island_selected_2 = db.Column(db.Boolean, default=False)
    is_exhibition_selected_2 = db.Column(db.Boolean, default=False)
    is_clock_museum_selected_2 = db.Column(db.Boolean, default=False)

    name_3 = db.Column(db.String(20), nullable=True)
    id_card_3 = db.Column(db.String(50), nullable=True)
    id_type_3 = db.Column(db.Integer, default=0)
    audience_ticket_type_id_3_id = db.Column(db.Integer, ForeignKey('TicketTypes.ticket_type_id'), default=1)
    is_treasure_island_selected_3 = db.Column(db.Boolean, default=False)
    is_exhibition_selected_3 = db.Column(db.Boolean, default=False)
    is_clock_museum_selected_3 = db.Column(db.Boolean, default=False)

    name_4 = db.Column(db.String(20), nullable=True)
    id_card_4 = db.Column(db.String(50), nullable=True)
    id_type_4 = db.Column(db.Integer, default=0)
    audience_ticket_type_id_4_id = db.Column(db.Integer, ForeignKey('TicketTypes.ticket_type_id'), default=1)
    is_treasure_island_selected_4 = db.Column(db.Boolean, default=False)
    is_exhibition_selected_4 = db.Column(db.Boolean, default=False)
    is_clock_museum_selected_4 = db.Column(db.Boolean, default=False)

    name_5 = db.Column(db.String(20), nullable=True)
    id_card_5 = db.Column(db.String(50), nullable=True)
    id_type_5 = db.Column(db.Integer, default=0)
    audience_ticket_type_id_5_id = db.Column(db.Integer, ForeignKey('TicketTypes.ticket_type_id'), default=1)
    is_treasure_island_selected_5 = db.Column(db.Boolean, default=False)
    is_exhibition_selected_5 = db.Column(db.Boolean, default=False)
    is_clock_museum_selected_5 = db.Column(db.Boolean, default=False)


class BookingRecord(db.Model):
    __tablename__ = 'BookingRecords'
    __bind_key__ = 'museum_db'
    record_id = db.Column(db.Integer, primary_key=True)  # 订票记录ID
    user_id = db.Column(db.String(128), ForeignKey('Users.user_id'))
    user = relationship('User', back_populates='booking_records')
    order_id = db.Column(db.Integer, ForeignKey('Orders.order_id'))
    order = relationship('Order', back_populates='booking_records')
    quantity = db.Column(db.Integer, default=0)
    purchase_date = db.Column(db.String(50), nullable=True)


# 销售数据模块
class TicketSalesData(db.Model):
    __tablename__ = 'TicketSalesData'
    __bind_key__ = 'museum_db'
    id = db.Column(db.Integer, primary_key=True)  # 主键ID
    amount = db.Column(db.Numeric(10, 2), default=0.00)  # 销售总金额
    sale_date = db.Column(db.Date, nullable=False)  # 销售日期
    select_time = db.Column(db.String(10))  # 选择时间（上午或下午）
    gugong_ticket_count = db.Column(db.Integer, default=0)  # 故宫门票的数量
    treasure_island_ticket_count = db.Column(db.Integer, default=0)  # 珍宝岛门票的数量
    clock_museum_ticket_count = db.Column(db.Integer, default=0)  # 钟表馆门票的数量
    exhibition_ticket_count = db.Column(db.Integer, default=0)  # 展览的数量

    __table_args__ = (db.UniqueConstraint('sale_date', 'select_time'),)  # 确保同一天同一时间段唯一


class DailyTicketSale(db.Model):
    __tablename__ = 'DailyTicketSale'
    __bind_key__ = 'museum_db'
    id = db.Column(db.Integer, primary_key=True)  # 主键ID
    ticket_type_id = db.Column(db.Integer, ForeignKey('TicketTypes.ticket_type_id'))  # 门票类型ID，关联TicketType模型
    type_name = db.Column(db.String(30))  # 类型名称
    date = db.Column(db.Date, nullable=False)  # 售卖日期
    select_time = db.Column(db.String(10))  # 选择时间（上午或下午）
    ticket_count = db.Column(db.Integer, default=0)  # 售卖的数量
    total_amount = db.Column(db.Numeric(10, 2), default=0.00)  # 售卖的金额

    __table_args__ = (db.UniqueConstraint('ticket_type_id', 'date', 'select_time'),)  # 确保同一天同一时间段唯一


# 每日余票更新模块
class DailyTicketQuota(db.Model):
    __tablename__ = 'DailyTicketQuota'
    __bind_key__ = 'museum_db'
    id = db.Column(db.Integer, primary_key=True)  # 主键ID
    museum_ticket_type = db.Column(db.String(30))  # 类型名称
    date = db.Column(db.Date, nullable=False)  # 日期
    available_tickets = db.Column(db.Integer, default=0)  # 可用余票数量
    select_time = db.Column(db.String(10))  # 选择时间（上午或下午)


# 年票模块
class YearTicketQuota(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 主键ID
    user_id = db.Column(db.String(128), ForeignKey('Users.user_id'))
    available_tickets = db.Column(db.Integer, default=0)  # 整数类型，表示可用余票数量，默认值为 0

    __tablename__ = 'YearTicketQuota'


class YearTicketData(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 主键ID
    type_name = db.Column(db.String(30))  # 字符串，最大长度为 30
    date = db.Column(db.Date, nullable=False)  # 日期
    select_time = db.Column(db.String(10))  # 字符串，最大长度为 10
    ticket_count = db.Column(db.Integer, default=0)  # 整数，默认值为 0

    __tablename__ = 'YearTicketData'
    __table_args__ = (
        db.UniqueConstraint('date', 'select_time', name='unique_date_select_time'),  # 唯一约束
    )

