from flask import Blueprint, render_template, request, jsonify
from applications.common.utils.rights import authorize
from applications.models.gugong import DailyTicketQuota
from applications.extensions import db  # 导入数据库实例
from datetime import datetime
from sqlalchemy import extract

bp = Blueprint('insert_ticket_data', __name__, url_prefix='/insert_ticket_data')


# 售票信息管理
@bp.get('/')
@authorize("system:insert_ticket_data:main")
def main():
    return render_template('system/insert_ticket_data/main.html')


@bp.get('/query')
@authorize("system:insert_ticket_data:query")
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
        sales_query = db.session.query(DailyTicketQuota).filter(DailyTicketQuota.date == query_date_obj)

    elif query_type == 'month':
        # 按月查询（提取年月）
        sales_query = db.session.query(DailyTicketQuota).filter(
            extract('year', DailyTicketQuota.date) == query_date_obj.year,
            extract('month', DailyTicketQuota.date) == query_date_obj.month
        )

    else:
        return jsonify({"error": "无效的查询类型"}), 400

    # 如果选择了时间段，添加时间段过滤条件
    if select_time:
        sales_query = sales_query.filter(DailyTicketQuota.select_time == select_time)

    # 执行查询
    sales_data = sales_query.all()

    # 将查询结果转换为 JSON 格式
    result = []
    for sale in sales_data:
        result.append({
            "date": sale.date.strftime('%Y-%m-%d'),
            "select_time": sale.select_time,
            "museum_ticket_type": sale.museum_ticket_type,
            "available_tickets": sale.available_tickets,
        })

    return jsonify({"data": result}), 200


@bp.route('/update_quota', methods=['POST'])
@authorize("system:insert_ticket_data:update")
def update_quota():
    try:
        # 从请求中获取数据
        data = request.get_json()

        date = data.get('date')
        select_time = data.get('select_time')
        museum_ticket_type = data.get('museum_ticket_type')
        remaining_tickets = data.get('remaining_tickets')

        # 查找相应的票务记录
        quota = db.session.query(DailyTicketQuota).filter(
            DailyTicketQuota.date == date,
            DailyTicketQuota.select_time == select_time,
            DailyTicketQuota.museum_ticket_type == museum_ticket_type
        ).first()

        if quota:
            # 更新余票量
            quota.available_tickets = remaining_tickets
            db.session.commit()  # 提交更改到数据库
            return jsonify({"message": "余票量更新成功！"}), 200
        else:
            return jsonify({"message": "记录未找到！"}), 404
    except Exception as e:
        db.session.rollback()  # 发生错误时回滚
        print('发生错误:', str(e))  # 打印错误信息
        return jsonify({"message": "更新失败", "error": str(e)}), 500


@bp.route('/create_new', methods=['POST'])
@authorize("system:insert_ticket_data:create_new")
def create_new():
    try:
        # 从请求中获取数据
        data = request.get_json()

        date = data.get('date')
        select_time = data.get('select_time')

        # 创建四个数据记录
        museum_types = ['故宫', '珍宝馆', '钟表馆', '展览']
        for museum_type in museum_types:
            new_quota = DailyTicketQuota(
                date=date,
                select_time=select_time,
                museum_ticket_type=museum_type,
                available_tickets=0  # 初始余票量为0
            )
            db.session.add(new_quota)  # 添加到会话

        db.session.commit()  # 提交会话，保存到数据库

        return jsonify({"message": "新建成功！"}), 201  # 返回201 Created状态

    except Exception as e:
        db.session.rollback()  # 出错时回滚会话
        print(f"错误信息: {e}")  # 打印错误信息（可选）
        return jsonify({"message": "新建失败，请重试。", "error": str(e)}), 500  # 返回500错误状态


