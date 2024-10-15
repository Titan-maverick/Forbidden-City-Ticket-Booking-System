from flask import Blueprint, render_template, request, jsonify
from applications.common.utils.rights import authorize
from applications.models.gugong import DailyTicketSale
from applications.extensions import db  # 导入数据库实例
from datetime import datetime
from sqlalchemy import extract

bp = Blueprint('query_sale_detail', __name__, url_prefix='/query_sale_detail')


# 售票信息管理
@bp.get('/')
@authorize("system:query_sale_detail:main")
def main():
    return render_template('system/query_sale_detail/main.html')


@bp.get('/query')
@authorize("system:query_sale_detail:query")
def get_sale_data():
    # 获取查询参数
    query_type = request.args.get('type', 'day')  # 查询类型，默认为按日查询
    query_date = request.args.get('date')  # 获取传入的日期参数
    select_time = request.args.get('select_time')  # 获取传入的时间段参数

    if not query_date:
        return jsonify({"error": "日期不能为空"}), 400

    try:
        # 将传入的日期转换为 datetime 对象
        query_date_obj = datetime.strptime(query_date, '%Y-%m-%d')
    except ValueError:
        return jsonify({"error": "无效的日期格式，应为 YYYY-MM-DD"}), 400

    # 基于查询类型执行不同的查询
    if query_type == 'day':
        # 按日查询
        sales_query = db.session.query(DailyTicketSale).filter(DailyTicketSale.date == query_date_obj)

    elif query_type == 'month':
        # 按月查询（提取年月）
        sales_query = db.session.query(DailyTicketSale).filter(
            extract('year', DailyTicketSale.date) == query_date_obj.year,
            extract('month', DailyTicketSale.date) == query_date_obj.month
        )

    elif query_type == 'year':
        # 按年查询（提取年份）
        sales_query = db.session.query(DailyTicketSale).filter(
            extract('year', DailyTicketSale.date) == query_date_obj.year
        )
    else:
        return jsonify({"error": "无效的查询类型"}), 400

    # 如果选择了时间段，添加时间段过滤条件
    if select_time:
        sales_query = sales_query.filter(DailyTicketSale.select_time == select_time)

    # 执行查询
    sales_data = sales_query.all()

    # 将查询结果转换为 JSON 格式
    result = []
    for sale in sales_data:
        result.append({
            "date": sale.date.strftime('%Y-%m-%d'),
            "select_time": sale.select_time,
            "type_name": sale.type_name,
            "ticket_count": sale.ticket_count,
            "total_amount": sale.total_amount,
        })

    return jsonify({"data": result}), 200
