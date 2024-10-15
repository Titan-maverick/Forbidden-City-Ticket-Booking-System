use museum;


select *
from Users;
-- 删除用户电话测试数据
UPDATE Users
SET phone_number=''
WHERE user_id = 'ovKl_7Ry0pedE5MEog4iZJcPu2zY'; select *from Users;


select *
from frequentvisitors;

-- 插入常用观众信息表测试数据
INSERT INTO FrequentVisitors (user_id, name_1, id_card_1, name_2, id_card_2, name_3, id_card_3, name_4, id_card_4, name_5, id_card_5)
VALUES ('ovKl_7Ry0pedE5MEog4iZJcPu2zY', 'name_1', 'id_card_1', 'name_2', 'id_card_2', '', '', '', '', '', '');

-- 更新常用观众信息表测试数据
UPDATE FrequentVisitors
SET user_id='ovKl_7Ry0pedE5MEog4iZJcPu2zY', 
	name_1='test_1', id_card_1='123321123321123',id_type_1='0', 
    name_2='test_2', id_card_2='456321123321456',id_type_2='1', 
    name_3='test_3', id_card_3='789321123321654',id_type_3='2', 
    name_4='test_4', id_card_4='987321123321123',id_type_4='3', 
    name_5='test_5', id_card_5='654321123321789',id_type_5='4'
WHERE user_id = 'ovKl_7Ry0pedE5MEog4iZJcPu2zY'; select *from frequentvisitors;






SELECT @@global.time_zone, @@session.time_zone;
SET GLOBAL time_zone = 'UTC';

SELECT @@global.time_zone, @@session.time_zone;
SET GLOBAL time_zone = 'Asia/Shanghai';
