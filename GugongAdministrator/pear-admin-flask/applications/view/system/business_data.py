from flask import Blueprint, render_template, request, jsonify
from applications.common.utils.rights import authorize
from applications.models.gugong import TicketSalesData
from applications.extensions import db  # 导入数据库实例
from datetime import datetime
from sqlalchemy import func


bp = Blueprint('business_data', __name__, url_prefix='/business_data')


# 售票信息管理
@bp.get('/')
@authorize("system:business_data:main")
def main():
    return render_template('system/business_data/main.html')


@bp.get('/query')
@authorize("system:business_data:query")
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
        func.sum(TicketSalesData.amount).label('total_amount'),
        func.sum(TicketSalesData.gugong_ticket_count).label('total_gugong'),
        func.sum(TicketSalesData.treasure_island_ticket_count).label('total_treasure_island'),
        func.sum(TicketSalesData.clock_museum_ticket_count).label('total_clock_museum'),
        func.sum(TicketSalesData.exhibition_ticket_count).label('total_exhibition')
    ).filter(
        TicketSalesData.sale_date.between(start_date_obj, end_date_obj)  # 过滤日期范围
    )
    print('query', query)
    # 根据时间段选择添加条件
    if select_time == '上午':
        query = query.filter(TicketSalesData.select_time == '上午')
    elif select_time == '下午':
        query = query.filter(TicketSalesData.select_time == '下午')

    # 执行查询
    result = query.one_or_none()  # 使用 one_or_none() 来处理没有结果的情况
    # 构建响应数据
    if result:
        response_data = {
            "start_date": start_date,
            "end_date": end_date,
            "select_time": select_time,
            "total_amount": result.total_amount or 0,
            "total_gugong": result.total_gugong or 0,
            "total_treasure_island": result.total_treasure_island or 0,
            "total_clock_museum": result.total_clock_museum or 0,
            "total_exhibition": result.total_exhibition or 0,
        }
    else:
        response_data = {
            "start_date": start_date,
            "end_date": end_date,
            "select_time": select_time,
            "total_amount": 0,
            "total_gugong": 0,
            "total_treasure_island": 0,
            "total_clock_museum": 0,
            "total_exhibition": 0,
        }

    return jsonify({"data": response_data}), 200

