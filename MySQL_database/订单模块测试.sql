use museum;
-- 订票模块

-- 门票类型
select *
from TicketTypes;

-- 订单
select *
from orders;

-- 订票记录
select *
from BookingRecords;

-- 订单详情
select *
from OrderDetails;

-- (宏观)售票数据
select *
from TicketSalesData;

SET SQL_SAFE_UPDATES = 0;

INSERT INTO TicketTypes (ticket_type_id, type_name, description, price)
VALUES (14, '故宫年票', '', 0.00);

