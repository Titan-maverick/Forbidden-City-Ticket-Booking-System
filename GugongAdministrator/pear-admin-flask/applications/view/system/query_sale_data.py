from flask import Blueprint, render_template, request, jsonify
from applications.common.utils.rights import authorize
from applications.models.gugong import TicketSalesData
from applications.extensions import db  # 导入数据库实例
from datetime import datetime
from sqlalchemy import extract

bp = Blueprint('query_sale_data', __name__, url_prefix='/query_sale_data')


# 售票信息管理
@bp.get('/')
@authorize("system:query_sale_data:main")
def main():
    return render_template('system/query_sale_data/main.html')


@bp.get('/query')
@authorize("system:query_sale_data:query")
def get_sale_data():
    # 获取查询参数
    query_type = request.args.get('type', 'day')  # 查询类型，默认为按日查询
    query_date = request.args.get('date')  # 获取传入的日期参数

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
        sales_data = db.session.query(TicketSalesData).filter(TicketSalesData.sale_date == query_date_obj).all()
    elif query_type == 'month':
        # 按月查询（提取年月）
        sales_data = db.session.query(TicketSalesData).filter(
            extract('year', TicketSalesData.sale_date) == query_date_obj.year,
            extract('month', TicketSalesData.sale_date) == query_date_obj.month
        ).all()
    elif query_type == 'year':
        # 按年查询（提取年份）
        sales_data = db.session.query(TicketSalesData).filter(
            extract('year', TicketSalesData.sale_date) == query_date_obj.year
        ).all()
    else:
        return jsonify({"error": "无效的查询类型"}), 400

    # 将查询结果转换为 JSON 格式
    result = []
    for sale in sales_data:
        result.append({
            "sale_date": sale.sale_date.strftime('%Y-%m-%d'),
            "select_time": sale.select_time,
            "amount": sale.amount,
            "gugong_ticket_count": sale.gugong_ticket_count,
            "treasure_island_ticket_count": sale.treasure_island_ticket_count,
            "clock_museum_ticket_count": sale.clock_museum_ticket_count,
            "exhibition_ticket_count": sale.exhibition_ticket_count,
        })

    return jsonify({"data": result}), 200
