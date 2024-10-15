from flask import Blueprint, render_template, request, jsonify
from applications.common.utils.rights import authorize
from applications.models.gugong import DailyTicketSale
from applications.extensions import db  # 导入数据库实例
from datetime import datetime
from sqlalchemy import func


bp = Blueprint('business_data_detail', __name__, url_prefix='/business_data_detail')


# 售票信息管理
@bp.get('/')
@authorize("system:business_data_detail:main")
def main():
    return render_template('system/business_data_detail/main.html')


@bp.get('/query')
@authorize("system:business_data_detail:query")
def get_sale_data():
    # 获取查询参数
    start_date = request.args.get('start_date')  # 获取起始日期
    end_date = request.args.get('end_date')  # 获取结束日期
    select_time = request.args.get('select_time', '全天')  # 时间段，默认为全天

    # 检查日期是否为空
    if not start_date or not end_date:
        return jsonify({"error": "起始日期和结束日期不能为空"}), 400

    try:
        # 将传入的日期字符串转换为 datetime 对象
        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
        end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError:
        return jsonify({"error": "无效的日期格式，应为 YYYY-MM-DD"}), 400

    # 构建查询条件
    query = db.session.query(
        DailyTicketSale.ticket_type_id,  # 根据票种分组
        DailyTicketSale.type_name,  # 获取票种名称
        db.func.sum(DailyTicketSale.ticket_count).label('total_ticket_count'),  # 求和票数
        db.func.sum(DailyTicketSale.total_amount).label('total_ticket_amount')  # 求和票金额
    ).filter(
        DailyTicketSale.date.between(start_date_obj, end_date_obj)  # 过滤日期范围
    ).group_by(
        DailyTicketSale.ticket_type_id,  # 按票种分组
        DailyTicketSale.type_name
    )

    # 根据时间段选择添加条件
    if select_time == '上午':
        query = query.filter(DailyTicketSale.select_time == '上午')
    elif select_time == '下午':
        query = query.filter(DailyTicketSale.select_time == '下午')

    # 执行查询
    results = query.all()  # 获取所有结果
    print('results', results)

    # 构建响应数据
    response_data = []
    for result in results:
        response_data.append({
            "start_date": start_date,
            "end_date": end_date,
            "select_time": select_time,
            'type_name': result.type_name,
            'total_ticket_count': result.total_ticket_count,
            'total_ticket_amount': result.total_ticket_amount,
        })

    return jsonify({"data": response_data}), 200


