use museum;
-- 售票信息

-- 详细销量
select *
from DailyTicketSale
WHERE type_name = '学生票' and select_time = '上午';

SET SQL_SAFE_UPDATES = 0;
DELETE FROM DailyTicketSale
WHERE select_time = '下午';

-- (宏观)售票数据
select *
from ticketsalesdata
WHERE sale_date = '2024-10-13' and select_time = '下午';

-- 每日票量
select *
from DailyTicketQuota
WHERE date = '2024-10-13' and select_time = '下午';
