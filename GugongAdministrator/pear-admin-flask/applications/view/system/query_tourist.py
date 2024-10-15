from flask import Blueprint, render_template, request, jsonify
from applications.common.utils.rights import authorize
from applications.models.gugong import User, FrequentVisitor, OrderDetail
from applications.extensions import db  # 导入数据库实例
from sqlalchemy import or_, and_

bp = Blueprint('query_information', __name__, url_prefix='/query_information')


# 游客信息管理
@bp.get('/')
@authorize("system:query_information:main")
def main():
    return render_template('system/query_information/main.html')


# 用户分页查询
@bp.get('/data')
@authorize("system:query_information:data")
def get_frequentVisitor_data():
    # 获取请求参数
    real_name = request.args.get('realname', type=str)
    idNumber = request.args.get('idNumber', type=str)

    filters = []

    # 动态构建查询条件
    if real_name and not idNumber:
        filters.append(
            or_(
                FrequentVisitor.name_1.like(f"%{real_name}%"),
                FrequentVisitor.name_2.like(f"%{real_name}%"),
                FrequentVisitor.name_3.like(f"%{real_name}%"),
                FrequentVisitor.name_4.like(f"%{real_name}%"),
                FrequentVisitor.name_5.like(f"%{real_name}%"),
            )
        )

    if not real_name and idNumber:
        filters.append(
            or_(
                FrequentVisitor.id_card_1.like(f"%{idNumber}%"),
                FrequentVisitor.id_card_2.like(f"%{idNumber}%"),
                FrequentVisitor.id_card_3.like(f"%{idNumber}%"),
                FrequentVisitor.id_card_4.like(f"%{idNumber}%"),
                FrequentVisitor.id_card_5.like(f"%{idNumber}%"),
            )
        )

    # 如果同时有 real_name 和 idNumber
    if real_name and idNumber:
        filters.append(
            or_(
                and_(
                    FrequentVisitor.name_1.like(f"%{real_name}%"),
                    FrequentVisitor.id_card_1.like(f"%{idNumber}%")
                ),
                and_(
                    FrequentVisitor.name_2.like(f"%{real_name}%"),
                    FrequentVisitor.id_card_2.like(f"%{idNumber}%")
                ),
                and_(
                    FrequentVisitor.name_3.like(f"%{real_name}%"),
                    FrequentVisitor.id_card_3.like(f"%{idNumber}%")
                ),
                and_(
                    FrequentVisitor.name_4.like(f"%{real_name}%"),
                    FrequentVisitor.id_card_4.like(f"%{idNumber}%")
                ),
                and_(
                    FrequentVisitor.name_5.like(f"%{real_name}%"),
                    FrequentVisitor.id_card_5.like(f"%{idNumber}%")
                ),
            )
        )

    # 执行查询并分页
    query = db.session.query(FrequentVisitor).filter(*filters).distinct() if filters else db.session.query(FrequentVisitor).distinct()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    paginated_result = query.paginate(page=page, per_page=per_page, error_out=False)

    # 根据查询结果构建返回数据
    result = []
    for visitor in paginated_result.items:
        for i in range(1, 6):  # 1到5对应 name_1 到 name_5
            name_field = getattr(visitor, f'name_{i}')
            id_card_field = getattr(visitor, f'id_card_{i}')
            id_type_field = getattr(visitor, f'id_type_{i}')

            # 只有同时满足 real_name 和 idNumber 时才添加结果
            if real_name and idNumber:
                if name_field and real_name in name_field and id_card_field and idNumber in id_card_field:
                    result.append({
                        'name': name_field,
                        'id_type': id_type_field,
                        'id_card': id_card_field,
                    })
            # 处理只根据 real_name 或 idNumber 的情况
            elif (real_name and name_field and real_name in name_field) or (idNumber and id_card_field and idNumber in id_card_field):
                result.append({
                    'name': name_field,
                    'id_type': id_type_field,
                    'id_card': id_card_field,
                })

    return jsonify({
        'data': result,
        'count': paginated_result.total
    })


@bp.get('/order')
@authorize("system:query_information:order")
def get_order_data():
    # 获取请求参数
    order_number = request.args.get('order_number', type=str)

    # 查询与订单号对应的订单详情
    order_details = db.session.query(OrderDetail).filter_by(order_id=order_number).all()

    # 用于存储符合条件的记录
    result = []

    # 遍历所有订单详情
    for order in order_details:
        for i in range(1, 6):  # 1到5对应 name_1 到 name_5
            name_field = getattr(order, f'name_{i}', None)
            id_card_field = getattr(order, f'id_card_{i}', None)
            id_type_field = getattr(order, f'id_type_{i}', None)

            # 只保留 name 和 IDNumber 不为空的记录
            if name_field and id_card_field:
                result.append({
                    'name': name_field,
                    'id_card': id_card_field,
                    'id_type': id_type_field  # 证件类型
                })

    # 返回数据和总数
    return jsonify({
        'data': result,
        'count': len(result)  # 返回结果的总数
    })


@bp.get('/phone')
@authorize("system:query_information:phone")
def get_phone_data():
    phone = request.args.get('phone', type=str)

    # 确保传入的电话号码不为空
    if not phone:
        return jsonify({'error': '电话号码不能为空'}), 400

    # 从 User 表中获取对应电话号码的 UserID
    user = db.session.query(User).filter_by(phone_number=phone).first()  # 使用 first() 来获取单个用户
    if not user:
        return jsonify({'data': [], 'count': 0}), 200  # 如果找不到用户，返回空结果

    user_id = user.user_id  # 获取 UserID

    # 用于存储符合条件的记录
    result = []

    # 查找 FrequentVisitors 中与 UserID 相关的记录
    frequent_audiences = db.session.query(FrequentVisitor).filter_by(user_id=user_id).all()
    for audience in frequent_audiences:
        for i in range(1, 6):  # 1到5对应 name_1 到 name_5
            name_field = getattr(audience, f'name_{i}', None)
            id_card_field = getattr(audience, f'id_card_{i}', None)
            id_type_field = getattr(audience, f'id_type_{i}', None)

            # 只保留 name 和 IDNumber 不为空的记录
            if name_field and id_card_field:
                result.append({
                    'name': name_field,
                    'id_card': id_card_field,
                    'id_type': id_type_field  # 证件类型
                })

    # 返回数据和总数
    return jsonify({
        'data': result,
        'count': len(result)  # 返回结果的总数
    })

