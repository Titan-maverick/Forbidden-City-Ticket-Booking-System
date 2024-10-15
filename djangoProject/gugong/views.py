# 【**重要**】，函数。
import datetime
import json
from decimal import Decimal

import jwt
import pytz
import requests
from django.http import HttpResponse
from django.http import JsonResponse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from .models import User, Order, FrequentVisitor, BookingRecord, OrderDetail, TicketType, DailyTicketQuota, \
    TicketSalesData, DailyTicketSale

# Create your views here.

# 获取当前时间并转换为北京时区
beijing_tz = pytz.timezone('Asia/Shanghai')

SECRET_KEY = 'shujukushejigugong'


# 测试
def success_view(request):
    return HttpResponse('连接成功')


# 解码
def decode_jwt_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['user_id']  # 返回用户 ID
    except jwt.ExpiredSignatureError:
        return None  # 令牌已过期
    except jwt.InvalidTokenError:
        return None  # 令牌无效


# 微信登录
@method_decorator(csrf_exempt, name='dispatch')
class WeChatLoginView(View):
    def post(self, request):
        try:
            # 确保将请求体解析为 JSON 字典
            body = json.loads(request.body.decode('utf-8'))  # 将请求体转为 JSON 字典
            code = body.get('code')  # 获取 code
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        if not code:
            return JsonResponse({'error': 'No code provided'}, status=400)

        # 替换为你的微信小程序 appid 和 secret
        appid = 'wx484ff8f086174875'
        secret = '043d447726f838fec53c4308aac0ab1a'
        url = (f'https://api.weixin.qq.com/sns/jscode2session?appid={appid}&secret={secret}&js_code={code}&grant_type'
               f'=authorization_code')

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as e:
            return JsonResponse({'error': str(e)}, status=500)

        if 'errcode' in data:
            return JsonResponse({'error': data['errmsg']}, status=400)

        # 获取 openid 和 session_key
        openid = data['openid']
        visitors_data = []

        # 这里可以根据 openid 查找或创建用户
        user, created = User.objects.get_or_create(user_id=openid)

        # 生成 JWT 令牌
        token = self.create_jwt_token(openid)

        # 查询常用观众信息
        frequent_visitors, created = FrequentVisitor.objects.get_or_create(user=user)
        frequent_visitors = FrequentVisitor.objects.filter(user__user_id=openid)

        for visitor in frequent_visitors:
            visitors_data.append({
                'name_1': visitor.name_1,
                'id_card_1': visitor.id_card_1,
                'id_type_1': visitor.id_type_1,
                'name_2': visitor.name_2,
                'id_card_2': visitor.id_card_2,
                'id_type_2': visitor.id_type_2,
                'name_3': visitor.name_3,
                'id_card_3': visitor.id_card_3,
                'id_type_3': visitor.id_type_3,
                'name_4': visitor.name_4,
                'id_card_4': visitor.id_card_4,
                'id_type_4': visitor.id_type_4,
                'name_5': visitor.name_5,
                'id_card_5': visitor.id_card_5,
                'id_type_5': visitor.id_type_5,
            })
        # 获取所有 TicketType 信息
        ticket_types = list(TicketType.objects.all().values())
        return JsonResponse({
            'message': '登录成功',
            'phone_number': user.phone_number,  # 返回用户电话号码
            'frequent_visitors': visitors_data,  # 返回常用观众信息
            'token': token,  # 返回 JWT 令牌
            'ticket_types': ticket_types
        })

    def create_jwt_token(self, openid):
        payload = {
            'user_id': openid,
            'exp': timezone.now() + datetime.timedelta(days=1)  # 令牌有效期为1天
        }
        return jwt.encode(payload, SECRET_KEY, algorithm='HS256')


# 更新电话号码
@method_decorator(csrf_exempt, name='dispatch')
class UpdatePhoneView(View):
    def post(self, request):
        # 获取并解码 token
        token = request.headers.get('Authorization')
        if token and token.startswith('Bearer '):
            token = token.split(' ')[1]  # 获取实际的 token 部分
        if not token:
            return JsonResponse({'error': '未提供 token'}, status=401)

        try:
            openid = decode_jwt_token(token)
        except jwt.ExpiredSignatureError:
            print('Token expired')
            return JsonResponse({'error': '无效的 token'}, status=401)
        except jwt.InvalidTokenError as e:
            print('Invalid token error:', e)
            return JsonResponse({'error': '无效的 token'}, status=401)

        # 获取请求数据
        data = json.loads(request.body)
        phoneNumber = data.get('phoneNumber')

        # 根据 openid 更新数据库中的信息
        try:
            user = User.objects.get(user_id=openid)  # 查找用户
            user.phone_number = phoneNumber  # 更新 phone_number
            user.save()
        except FrequentVisitor.DoesNotExist:
            return JsonResponse({'error': '观众信息不存在'}, status=404)

        return JsonResponse({'message': '信息已更新'}, status=200)


# 更新常用观众信息
@method_decorator(csrf_exempt, name='dispatch')
class UpdateVisitorView(View):
    def post(self, request):
        # 获取并解码 token
        token = request.headers.get('Authorization')
        if token and token.startswith('Bearer '):
            token = token.split(' ')[1]  # 获取实际的 token 部分
        if not token:
            return JsonResponse({'error': '未提供 token'}, status=401)

        try:
            openid = decode_jwt_token(token)
        except jwt.ExpiredSignatureError:
            print('Token expired')
            return JsonResponse({'error': '无效的 token'}, status=401)
        except jwt.InvalidTokenError as e:
            print('Invalid token error:', e)
            return JsonResponse({'error': '无效的 token'}, status=401)

        # 获取请求数据
        data = json.loads(request.body)
        name = data.get('name')
        id_card = data.get('idCard')
        index = data.get('index')
        selectedIdTypeIndex = data.get('selectedIdTypeIndex')
        # 确保 index 是一位数，并拼接成对应字段
        index_str = str(index)

        # 根据 openid 更新数据库中的信息
        try:
            frequent_visitor = FrequentVisitor.objects.get(user_id=openid)  # 假设一个用户只对应一个 FrequentVisitor
            setattr(frequent_visitor, f'name_{index_str}', name)  # 更新对应的 name
            setattr(frequent_visitor, f'id_card_{index_str}', id_card)  # 更新对应的 id_card
            setattr(frequent_visitor, f'id_type_{index_str}', selectedIdTypeIndex)  # 更新对应的 id_type
            frequent_visitor.save()
        except FrequentVisitor.DoesNotExist:
            return JsonResponse({'error': '观众信息不存在'}, status=404)

        return JsonResponse({'message': '信息已更新'}, status=200)


# 删除常用观众信息
@method_decorator(csrf_exempt, name='dispatch')
class DeleteVisitorView(View):
    def post(self, request):
        # 获取并解码 token
        token = request.headers.get('Authorization')
        if token and token.startswith('Bearer '):
            token = token.split(' ')[1]  # 获取实际的 token 部分
        if not token:
            return JsonResponse({'error': '未提供 token'}, status=401)

        try:
            openid = decode_jwt_token(token)
        except jwt.ExpiredSignatureError:
            print('Token expired')
            return JsonResponse({'error': '无效的 token'}, status=401)
        except jwt.InvalidTokenError as e:
            print('Invalid token error:', e)
            return JsonResponse({'error': '无效的 token'}, status=401)

        # 获取请求数据
        data = json.loads(request.body)
        selectedIdTypeIndex = data.get('selectedIdTypeIndex')
        index = data.get('index')

        # 确保 index 是一位数，并拼接成对应字段
        index_str = int(index)
        visitors_data = []
        # 根据 openid 更新数据库中的信息
        try:
            frequent_visitor = FrequentVisitor.objects.get(user_id=openid)  # 假设一个用户只对应一个 FrequentVisitor

            if 0 < index_str < 5:
                # 向前移动数据
                for i in range(index_str, 5):
                    setattr(frequent_visitor, f'name_name_{i}', getattr(frequent_visitor, f'name_{i + 1}'))
                    setattr(frequent_visitor, f'id_card_{i}', getattr(frequent_visitor, f'id_card_{i + 1}'))
                    setattr(frequent_visitor, f'id_type_{i}', getattr(frequent_visitor, f'id_type_{i + 1}'))

                # 最后一个位置清空
                setattr(frequent_visitor, f'name_5', '')
                setattr(frequent_visitor, f'id_card_5', '')
                setattr(frequent_visitor, f'id_type_5', 0)

            elif index_str == 5:
                # 清空最后一个位置
                setattr(frequent_visitor, f'name_{index_str}', '')
                setattr(frequent_visitor, f'id_card_{index_str}', '')
                setattr(frequent_visitor, f'id_type_5', 0)

            frequent_visitor.save()
        except FrequentVisitor.DoesNotExist:
            return JsonResponse({'error': '观众信息不存在'}, status=404)
        frequent_visitors = FrequentVisitor.objects.filter(user__user_id=openid)

        for visitor in frequent_visitors:
            visitors_data.append({
                'name_1': visitor.name_1,
                'id_card_1': visitor.id_card_1,
                'id_type_1': visitor.id_type_1,
                'name_2': visitor.name_2,
                'id_card_2': visitor.id_card_2,
                'id_type_2': visitor.id_type_2,
                'name_3': visitor.name_3,
                'id_card_3': visitor.id_card_3,
                'id_type_3': visitor.id_type_3,
                'name_4': visitor.name_4,
                'id_card_4': visitor.id_card_4,
                'id_type_4': visitor.id_type_4,
                'name_5': visitor.name_5,
                'id_card_5': visitor.id_card_5,
                'id_type_5': visitor.id_type_5,
            })
        return JsonResponse({'message': '信息已更新', 'frequent_visitors': visitors_data}, status=200)


# 添加访客信息
@method_decorator(csrf_exempt, name='dispatch')
class AddVisitorView(View):
    def post(self, request):
        # 获取并解码 token
        token = request.headers.get('Authorization')
        if token and token.startswith('Bearer '):
            token = token.split(' ')[1]  # 获取实际的 token 部分
        if not token:
            return JsonResponse({'error': '未提供 token'}, status=401)

        try:
            openid = decode_jwt_token(token)
        except jwt.ExpiredSignatureError:
            print('Token expired')
            return JsonResponse({'error': '无效的 token'}, status=401)
        except jwt.InvalidTokenError as e:
            print('Invalid token error:', e)
            return JsonResponse({'error': '无效的 token'}, status=401)

        # 获取请求数据
        data = json.loads(request.body)
        name = data.get('name')
        id_card = data.get('idCard')
        selectedIdTypeIndex = data.get('selectedIdTypeIndex')
        index = 0
        # 根据 openid 更新数据库中的信息
        try:
            frequent_visitor = FrequentVisitor.objects.get(user_id=openid)  # 假设一个用户只对应一个 FrequentVisitor

            # 检查 name_1 到 name_5 和 id_card_1 到 id_card_5 是否为空
            for i in range(1, 6):
                name_attr = getattr(frequent_visitor, f'name_{i}')
                id_card_attr = getattr(frequent_visitor, f'id_card_{i}')

                # 如果当前的 name 和 id_card 都为空，更新为新的值
                if not name_attr and not id_card_attr:
                    index = i
                    setattr(frequent_visitor, f'name_{i}', name)
                    setattr(frequent_visitor, f'id_card_{i}', id_card)
                    setattr(frequent_visitor, f'id_type_{i}', selectedIdTypeIndex)
                    break  # 找到第一个空位后跳出循环

            frequent_visitor.save()
        except FrequentVisitor.DoesNotExist:
            return JsonResponse({'error': '观众信息不存在'}, status=404)

        return JsonResponse({'message': '信息已更新', 'index': index}, status=200)


# 创建订单信息
@method_decorator(csrf_exempt, name='dispatch')
class ComfirmOrdersView(View):
    def post(self, request):
        # 获取并解码 token
        token = request.headers.get('Authorization')
        if token and token.startswith('Bearer '):
            token = token.split(' ')[1]  # 获取实际的 token 部分
        if not token:
            return JsonResponse({'error': '未提供 token'}, status=401)

        try:
            openid = decode_jwt_token(token)
        except jwt.ExpiredSignatureError:
            return JsonResponse({'error': '无效的 token'}, status=401)
        except jwt.InvalidTokenError as e:
            return JsonResponse({'error': '无效的 token'}, status=401)

        # 获取请求数据
        data = json.loads(request.body)

        # 提取数据
        audience_list = data.get('audienceList', [])
        phone_number = data.get('phoneNumber')
        total_price = data.get('totalPrice')
        selected_time = data.get('selectedTime')
        selected_date = data.get('selectedDate')
        purchaseQuantities = data.get('purchaseQuantities')
        # 根据 openid 获取 User 实例
        user = User.objects.get(user_id=openid)  # 查找用户

        # 解析字符串为日期对象
        date_obj = datetime.datetime.strptime(selected_date, "%Y年%m月%d日")
        # 格式化为 YYYY-MM-DD
        formatted_date = date_obj.strftime("%Y-%m-%d")

        # 更新售票数据
        sales_data, created = TicketSalesData.objects.get_or_create(
            sale_date=formatted_date,
            select_time=selected_time,
            defaults={
                'amount': 0,
                'gugong_ticket_count': 0,
                'treasure_island_ticket_count': 0,
                'clock_museum_ticket_count': 0,
                'exhibition_ticket_count': 0,
            }
        )
        quota = DailyTicketQuota.objects.get(museum_ticket_type='故宫', date=formatted_date, select_time=selected_time)
        quota_treasure = DailyTicketQuota.objects.get(museum_ticket_type='珍宝馆', date=formatted_date,
                                                      select_time=selected_time)
        quota_clock = DailyTicketQuota.objects.get(museum_ticket_type='钟表馆', date=formatted_date,
                                                   select_time=selected_time)
        quot_exhibition = DailyTicketQuota.objects.get(museum_ticket_type='展览', date=formatted_date,
                                                       select_time=selected_time)
        tickets_available = True

        # 用于更新每日销量(DailyTicketSale)
        daily_sales = {}  # 用于跟踪每日销量

        # 用事务管理保存操作
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

        # 更新每日票量(DailyTicketQuota)
        # 用事务管理保存操作
        try:
            with transaction.atomic():
                for audience in audience_list:
                    if quota.available_tickets > 0:
                        quota.available_tickets -= 1
                    else:
                        tickets_available = False
                        break  # 如果没有票了，停止处理
                    ticket_id = audience.get('ticketId')
                    isTreasureIslandSelected = audience.get('isTreasureIslandSelected')
                    isClockMuseumSelected = audience.get('isClockMuseumSelected')
                    isExhibitionSelected = audience.get('isExhibitionSelected')

                    # 根据票种更新售票数据(TicketSalesData)和每日销量(DailyTicketSale)
                    if tickets_available:
                        sales_data.gugong_ticket_count += 1
                        # 更新每日销量
                        ticket_type_ticket_id = TicketType.objects.get(ticket_type_id=ticket_id)
                        daily_sales[ticket_id] = DailyTicketSale.objects.get(
                            ticket_type=ticket_type_ticket_id,
                            date=formatted_date,
                            select_time=selected_time,
                        )
                        daily_sales[ticket_id].ticket_count = daily_sales[ticket_id].ticket_count + 1
                        ticket_type = TicketType.objects.get(ticket_type_id=ticket_id)
                        daily_sales[ticket_id].type_name = ticket_type.type_name
                        daily_sales[ticket_id].total_amount = Decimal(daily_sales[ticket_id].total_amount) + Decimal(
                            ticket_type.price)

                    if isTreasureIslandSelected:
                        if quota_treasure.available_tickets > 0:
                            quota_treasure.available_tickets -= 1
                        else:
                            tickets_available = False
                            break  # 如果没有票了，停止处理
                        sales_data.treasure_island_ticket_count += 1

                        # 更新每日销量
                        ticket_type_ticket_id = TicketType.objects.get(ticket_type_id=(ticket_id + 4))
                        daily_sales[ticket_id + 4], created = DailyTicketSale.objects.get_or_create(
                            ticket_type=ticket_type_ticket_id,
                            date=formatted_date,
                            select_time=selected_time,
                        )
                        daily_sales[ticket_id + 4].ticket_count = daily_sales[ticket_id + 4].ticket_count + 1
                        ticket_type = TicketType.objects.get(ticket_type_id=(ticket_id + 4))
                        daily_sales[ticket_id + 4].type_name = ticket_type.type_name
                        daily_sales[ticket_id + 4].total_amount = Decimal(daily_sales[ticket_id + 4].total_amount) + Decimal(
                            ticket_type.price)

                    if isClockMuseumSelected:
                        if quota_clock.available_tickets > 0:
                            quota_clock.available_tickets -= 1
                        else:
                            tickets_available = False
                            break  # 如果没有票了，停止处理
                        sales_data.clock_museum_ticket_count += 1
                        # 更新每日销量
                        ticket_type_ticket_id = TicketType.objects.get(ticket_type_id=(ticket_id + 8))
                        daily_sales[ticket_id + 8], created = DailyTicketSale.objects.get_or_create(
                            ticket_type=ticket_type_ticket_id,
                            date=formatted_date,
                            select_time=selected_time,
                        )
                        daily_sales[ticket_id + 8].ticket_count = daily_sales[ticket_id + 8].ticket_count + 1
                        ticket_type = TicketType.objects.get(ticket_type_id=(ticket_id + 8))
                        daily_sales[ticket_id + 8].type_name = ticket_type.type_name
                        daily_sales[ticket_id + 8].total_amount = Decimal(daily_sales[ticket_id + 8].total_amount) + Decimal(
                            ticket_type.price)

                    if isExhibitionSelected:
                        if quot_exhibition.available_tickets > 0:
                            quot_exhibition.available_tickets -= 1
                        else:
                            tickets_available = False
                            break  # 如果没有票了，停止处理
                        sales_data.exhibition_ticket_count += 1
                        # 更新每日销量
                        ticket_type_ticket_id = TicketType.objects.get(ticket_type_id=13)
                        daily_sales[13], created = DailyTicketSale.objects.get_or_create(
                            ticket_type=ticket_type_ticket_id,
                            date=formatted_date,
                            select_time=selected_time,
                        )
                        daily_sales[13].ticket_count = daily_sales[13].ticket_count + 1
                        ticket_type = TicketType.objects.get(ticket_type_id=13)
                        daily_sales[13].type_name = ticket_type.type_name
                        daily_sales[13].total_amount = Decimal(daily_sales[13].total_amount) + Decimal(
                            ticket_type.price)

                    # 保存所有更新后的 daily_sales
                    for daily_sale in daily_sales.values():
                        daily_sale.save()

                sales_data.amount += Decimal(total_price)  # 假设每种票的价格相同，计算金额

                # 仅在所有观众处理完且票仍可用时保存
                if tickets_available:
                    quota.save()
                    quota_treasure.save()
                    quota_clock.save()
                    quota_clock.save()
                    quot_exhibition.save()
                    sales_data.save()

                else:
                    return JsonResponse({'error': '票已售空'}, status=400)

        except Exception as e:
            print(f"Error occurred, rolling back changes: {e}")

        # 创建订单
        order = Order.objects.create(
            user=user,
            phone_number=phone_number,
            quantity=purchaseQuantities,
            status='待支付',
            order_date=f"{selected_date}",
            select_time=f"{selected_time}"
        )

        # 获取北京时间
        purchase_date = timezone.now().astimezone(pytz.timezone('Asia/Shanghai'))  # 获取当前时间并转换为北京时间
        # 格式化时间为 "YYYY年MM月DD日HH:MM"
        formatted_purchase_date = purchase_date.strftime('%Y年%m月%d日%H:%M')
        # 创建订票记录
        BookingRecord.objects.create(
            user=user,
            order=order,
            quantity=purchaseQuantities,
            purchase_date=formatted_purchase_date  # 记录购买时间
        )
        # 创建订单详情
        # 创建一个对应 order 的 OrderDetail 实例python manage.py makemigrations
        order_detail = OrderDetail.objects.create(order=order)

        # 更新 OrderDetail 数据
        for i in range(min(purchaseQuantities, len(audience_list))):
            audience = audience_list[i]
            ticket_type = TicketType.objects.get(ticket_type_id=audience.get('ticketId'))

            # 根据观众信息更新 OrderDetail 字段
            setattr(order_detail, f'name_{i + 1}', audience.get('name'))
            setattr(order_detail, f'id_card_{i + 1}', audience.get('idNumber'))
            setattr(order_detail, f'id_type_{i + 1}', audience.get('selectedIdTypeIndex', 0))
            setattr(order_detail, f'audience_ticket_type_id_{i + 1}', ticket_type)
            setattr(order_detail, f'is_clock_museum_selected_{i + 1}', audience.get('isClockMuseumSelected', False))
            setattr(order_detail, f'is_exhibition_selected_{i + 1}', audience.get('isExhibitionSelected', False))
            setattr(order_detail, f'is_treasure_island_selected_{i + 1}',
                    audience.get('isTreasureIslandSelected', False))

        # 保存更新后的 OrderDetail
        order_detail.save()

        return JsonResponse({'message': '订单创建成功', 'order_id': order.order_id}, status=201)


# 用户确认订单
@method_decorator(csrf_exempt, name='dispatch')
class PayView(View):
    def post(self, request):
        # 获取并解码 token
        token = request.headers.get('Authorization')
        if token and token.startswith('Bearer '):
            token = token.split(' ')[1]
        if not token:
            return JsonResponse({'error': '未提供 token'}, status=401)

        try:
            openid = decode_jwt_token(token)
        except jwt.ExpiredSignatureError:
            return JsonResponse({'error': '无效的 token'}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({'error': '无效的 token'}, status=401)

        # 修改用户的订单信息状态
        try:
            # 获取请求数据
            data = json.loads(request.body)
            order_id = data.get('order_id')

            # 查找并更新订单状态
            order = Order.objects.get(order_id=order_id)  # 根据订单 ID 查找订单
            order.status = '未使用'  # 修改状态
            order.save()  # 保存更改

            return JsonResponse({'message': '订单状态已更新'}, status=200)

        except Order.DoesNotExist:
            return JsonResponse({'error': '订单不存在'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': '请求体格式错误'}, status=400)


# 我的订单界面 获取用户订单信息
@method_decorator(csrf_exempt, name='dispatch')
class UserOrdersView(View):
    def post(self, request):
        # 获取并解码 token
        token = request.headers.get('Authorization')
        if token and token.startswith('Bearer '):
            token = token.split(' ')[1]
        if not token:
            return JsonResponse({'error': '未提供 token'}, status=401)

        try:
            openid = decode_jwt_token(token)
        except jwt.ExpiredSignatureError:
            return JsonResponse({'error': '无效的 token'}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({'error': '无效的 token'}, status=401)

        # 获取用户的订单信息
        try:
            user = User.objects.get(user_id=openid)
            orders = Order.objects.filter(user=user)
            orders_data = []

            for order in orders:
                booking_record = BookingRecord.objects.filter(order=order).first()
                order_details = list(order.orderdetail_set.values())
                # 获取第一个订单详情
                order_details = order_details[0]  # 获取列表中的第一个字典
                count = order.quantity
                order_info = {
                    'order_id': order.order_id,
                    'status': order.status,
                    'quantity': order.quantity,
                    'order_date': order.order_date,
                    'selected_time': order.select_time,
                    'booking_record': {
                        'purchase_date': booking_record.purchase_date if booking_record else None,
                    },
                    'audienceList': [
                        {
                            f'name': order_details[f'name_{i + 1}'],
                            f'id_card': order_details[f'id_card_{i + 1}'],
                            f'id_type': order_details[f'id_type_{i + 1}'],
                            f'ticket_type_id': order_details[f'audience_ticket_type_id_{i + 1}_id'],
                            f'isClockMuseumSelected': order_details[f'is_clock_museum_selected_{i + 1}'],
                            f'isExhibitionSelected': order_details[f'is_exhibition_selected_{i + 1}'],
                            f'isTreasureIslandSelected': order_details[f'is_treasure_island_selected_{i + 1}'],
                        } for i in range(count)
                    ],
                }
                orders_data.append(order_info)

            # 获取所有 TicketType 信息
            ticket_types = list(TicketType.objects.all().values())
            return JsonResponse({'orders': orders_data, 'ticket_types': ticket_types}, status=200)

        except User.DoesNotExist:
            return JsonResponse({'error': '用户不存在'}, status=404)


# 退票
@method_decorator(csrf_exempt, name='dispatch')
class RefundView(View):
    def post(self, request):
        # 获取并解码 token
        token = request.headers.get('Authorization')
        if token and token.startswith('Bearer '):
            token = token.split(' ')[1]
        if not token:
            return JsonResponse({'error': '未提供 token'}, status=401)

        try:
            openid = decode_jwt_token(token)
        except jwt.ExpiredSignatureError:
            return JsonResponse({'error': '无效的 token'}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({'error': '无效的 token'}, status=401)

        # 修改用户的订单信息状态
        try:
            # 获取请求数据
            data = json.loads(request.body)
            orderDetails = data.get('orderDetails')
            order_id = orderDetails.get('order_id')
            total_price = orderDetails.get('total')

            audience_list = orderDetails.get('audienceList')
            Concise_orders = orderDetails.get('concise_orders')
            selected_date = orderDetails.get('order_date')
            selected_time = orderDetails.get('selected_time')

            # 查找并更新订单状态
            order = Order.objects.get(order_id=order_id)  # 根据订单 ID 查找订单
            order.status = '已退票'  # 修改状态
            order.save()  # 保存更改

            # 解析字符串为日期对象
            date_obj = datetime.datetime.strptime(selected_date, "%Y年%m月%d日")
            # 格式化为 YYYY-MM-DD
            formatted_date = date_obj.strftime("%Y-%m-%d")

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
                            daily_sales[ticket_id].total_amount = Decimal(daily_sales[ticket_id].total_amount) - Decimal(
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
                            daily_sales[ticket_id + 4].total_amount = Decimal(daily_sales[ticket_id + 4].total_amount) - Decimal(
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
                            daily_sales[ticket_id + 8].total_amount = Decimal(daily_sales[ticket_id + 8].total_amount) - Decimal(
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
                        return JsonResponse({'error': '退票失败'}, status=400)
            except Exception as e:
                print(f"Error occurred, rolling back changes: {e}")

            return JsonResponse({'message': '订单状态已更新'}, status=200)

        except Order.DoesNotExist:
            return JsonResponse({'error': '订单不存在'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': '请求体格式错误'}, status=400)


# 获取可用余票
@method_decorator(csrf_exempt, name='dispatch')
class AvailableTicketsView(View):
    def post(self, request):
        # 获取并解码 token
        token = request.headers.get('Authorization')
        if token and token.startswith('Bearer '):
            token = token.split(' ')[1]  # 获取实际的 token 部分
        if not token:
            return JsonResponse({'error': '未提供 token'}, status=401)

        try:
            openid = decode_jwt_token(token)
        except jwt.ExpiredSignatureError:
            print('Token expired')
            return JsonResponse({'error': '无效的 token'}, status=401)
        except jwt.InvalidTokenError as e:
            print('Invalid token error:', e)
            return JsonResponse({'error': '无效的 token'}, status=401)

        # 获取请求数据
        data = json.loads(request.body)
        selectedDate = data.get('selectedDate')

        # 解析字符串为日期对象
        date_obj = datetime.datetime.strptime(selectedDate, "%Y年%m月%d日")
        # 格式化为 YYYY-MM-DD
        formatted_date = date_obj.strftime("%Y-%m-%d")

        # 根据 formatted_date 获取余票信息
        try:
            # 查询对应日期的票务信息
            morning_daily_quota = DailyTicketQuota.objects.get(
                museum_ticket_type='故宫', date=formatted_date, select_time='上午')
            afternoon_daily_quota = DailyTicketQuota.objects.get(
                museum_ticket_type='故宫', date=formatted_date, select_time='下午')

            response_data = {
                'morning_tickets_available': morning_daily_quota.available_tickets,
                'afternoon_tickets_available': afternoon_daily_quota.available_tickets
            }
            return JsonResponse(response_data, status=200)

        except DailyTicketQuota.DoesNotExist:
            return JsonResponse({'error': '该日期的票务信息不存在'}, status=404)


# 获取其他可用余票
@method_decorator(csrf_exempt, name='dispatch')
class OtherAvailableTicketsView(View):
    def post(self, request):
        # 获取并解码 token
        token = request.headers.get('Authorization')
        if token and token.startswith('Bearer '):
            token = token.split(' ')[1]  # 获取实际的 token 部分
        if not token:
            return JsonResponse({'error': '未提供 token'}, status=401)

        try:
            openid = decode_jwt_token(token)
        except jwt.ExpiredSignatureError:
            print('Token expired')
            return JsonResponse({'error': '无效的 token'}, status=401)
        except jwt.InvalidTokenError as e:
            print('Invalid token error:', e)
            return JsonResponse({'error': '无效的 token'}, status=401)

        # 获取请求数据
        data = json.loads(request.body)
        selectedDate = data.get('selectedDate')
        selectedTime = data.get('selectedTime')

        # 解析字符串为日期对象
        date_obj = datetime.datetime.strptime(selectedDate, "%Y年%m月%d日")
        # 格式化为 YYYY-MM-DD
        formatted_date = date_obj.strftime("%Y-%m-%d")

        # 根据 formatted_date 获取余票信息
        try:
            # 查询对应日期的票务信息
            treasure_daily_quota = DailyTicketQuota.objects.get(
                museum_ticket_type='珍宝馆', date=formatted_date, select_time=selectedTime)
            clock_daily_quota = DailyTicketQuota.objects.get(
                museum_ticket_type='钟表馆', date=formatted_date, select_time=selectedTime)
            exhibition_daily_quota = DailyTicketQuota.objects.get(
                museum_ticket_type='展览', date=formatted_date, select_time=selectedTime)

            response_data = {
                'treasure_tickets_available': treasure_daily_quota.available_tickets,
                'clock_tickets_available': clock_daily_quota.available_tickets,
                'exhibition_tickets_available': exhibition_daily_quota.available_tickets
            }
            return JsonResponse(response_data, status=200)

        except DailyTicketQuota.DoesNotExist:
            return JsonResponse({'error': '该日期的票务信息不存在'}, status=404)
