from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect, Http404, HttpResponse, render_to_response
from django_pandas.io import read_frame
import pandas as pd
import datetime
from station_data_overview.models import StationSalesOverall
from station_data_overview.models import OnlyStationInfo

"""
站点汇总数据总览, 一共分为3层级:
第1层级:
按照近1天，近7天，近14天，近30天全站点数据汇总
包含列:
类型，广告花费，广告销售额，站点销售额，站点数量，ACoS，销售占比，花费占比，异常数量
第2层级: (点击近1天，近7天，近14天，近30天跳转)
显示全部站点的数据，按照站点销售额降序排列
包含列:
账号，广告接手人，广告花费，广告销售额，站点销售额，站点数据，ACoS，销售占比，花费占比，异常预警
第3层级: (点击站点后显示站点详情)
显示改站点近1天，近7天，近14天，近30天的最近三项的比较
包含列:
账号，日期，广告接手人，广告花费(包含环比)，广告销售额(包含环比)，站点销售额(包含环比)，ACoS(包含环比)，销售占比(包含环比)，花费占比(包含环比)


    另外异常预警的逻辑:

        标准暂定	ACoS	销售占比	花费占比
        近1天	    20%	      -10%	        5%
        近7天	    10%	      -8%	        3%
        近14天	    7%	      -7%	        2%
        近30天	    5%	      -6%	        1%
"""


# Create your views here.


# 得到站点管理员信息
def get_mamager_info():
    manager_info = OnlyStationInfo.objects.all()
    manager_info = read_frame(manager_info)
    return manager_info


# 得到站点的汇总数据
def db_download_station_overview_ori():
    station_info_ori = StationSalesOverall.objects.all()
    station_info_ori = read_frame(station_info_ori)
    return station_info_ori


# 第1层级汇总:
def group_all_days(station_overview_ori):
    """
    汇总第一层级的数据
    :param station_overview_ori:站点汇总的原始数据
    :return:按照天数汇总后的数据
    """
    # 按天汇总
    # !!! 这里应该是今天的date !!!
    new_date = max(station_overview_ori['date'])

    def group_day(day_distance):
        """
        按照某一特定天数汇总
        :param day_before: 多少天以前 天数
        :return: 按照多少天以前汇总的数据
        """
        day_before = new_date - datetime.timedelta(days=day_distance)
        date_before_data = station_overview_ori[
            (station_overview_ori['date'] <= new_date) & (station_overview_ori['date'] > day_before)]
        station_num = len(date_before_data)
        if station_num == 0:
            return
        sum_ad_spend = int(sum(date_before_data['ad_spend']))
        sum_ad_sales = int(sum(date_before_data['ad_sales']))
        sum_shop_sales = int(sum(date_before_data['shop_sales']))
        if sum_ad_sales > 0:
            sum_acos = str(round(100 * sum_ad_spend / sum_ad_sales, 2)) + '%'
        else:
            sum_acos = '0.00%'
        if sum_shop_sales > 0:
            sum_sale_rate = str(round(100 * sum_ad_sales / sum_shop_sales, 2)) + '%'
            sum_spend_rate = str(round(100 * sum_ad_spend / sum_shop_sales, 2)) + '%'
        else:
            sum_spend_rate = '0%'
            sum_sale_rate = '0%'
        return [day_distance, sum_ad_spend, sum_ad_sales, sum_shop_sales, station_num, sum_acos, sum_sale_rate,
                sum_spend_rate]

    # 按天汇总
    group_date = [1, 7, 14, 30]
    all_days_group = [group_day(date) for date in group_date]
    all_days_group = pd.DataFrame(all_days_group,
                                  columns=['day_distance', 'ad_spend', 'ad_sales', 'shop_sales', 'station_num', 'acos',
                                           'sale_rate', 'spend_rate'])
    # print(all_days_group)

    return all_days_group


# 第2层级汇总
def group_all_stations(station_overview_ori, choose_day):
    """
    显示指定的天数下站点汇总数据
    :param station_overview_ori:原始数据
    :param choose_day:指定天数
    :return:
    """
    if (station_overview_ori.empty) or (station_overview_ori is None) or (
            not isinstance(station_overview_ori, pd.DataFrame)):
        return
    # !!! 这里应该是今天的date !!!
    # 得到管理员的数据
    manager_info = get_mamager_info()
    new_date = max(station_overview_ori['date'])
    first_date = new_date - datetime.timedelta(days=choose_day)
    station_overview_date_after = station_overview_ori[station_overview_ori['date'] > first_date]
    station_overview_date_after_group = station_overview_date_after.groupby('station').agg(
        {'ad_spend': 'sum', 'ad_sales': 'sum', 'shop_sales': 'sum'}).reset_index()
    station_overview_date_after_group[['ad_spend', 'ad_sales', 'shop_sales']] = station_overview_date_after_group[
        ['ad_spend', 'ad_sales', 'shop_sales']].applymap(lambda x: int(x))
    station_overview_date_after_group = pd.merge(station_overview_date_after_group,
                                                 manager_info[['station', 'ad_manger']], on='station', how='left')
    # 计算acos,spend_rate,sale_rate
    station_overview_date_after_group['acos'] = [str(round(100 * spend / sale, 2)) + '%' if sale > 0 else '0%' for
                                                 spend, sale in zip(station_overview_date_after_group['ad_spend'],
                                                                    station_overview_date_after_group['ad_sales'])]
    station_overview_date_after_group['spend_rate'] = [str(round(100 * spend / sale, 2)) + '%' if sale > 0 else '0%' for
                                                       spend, sale in zip(station_overview_date_after_group['ad_spend'],
                                                                          station_overview_date_after_group[
                                                                              'shop_sales'])]
    station_overview_date_after_group['sale_rate'] = [
        str(round(100 * ad_sale / shop_sale, 2)) + '%' if shop_sale > 0 else '0%' for
        ad_sale, shop_sale in
        zip(station_overview_date_after_group['ad_sales'], station_overview_date_after_group['shop_sales'])]
    station_overview_date_after_group = station_overview_date_after_group[
        ['station', 'ad_manger', 'ad_spend', 'ad_sales', 'shop_sales', 'acos', 'sale_rate', 'spend_rate']]
    station_overview_date_after_group.sort_values(by='shop_sales', ascending=False, inplace=True)
    return station_overview_date_after_group.head(20)


# 第3层级汇总
def group_station_day(station_overview_ori, station_name, choose_day):
    """
    对三层级汇总
    主要是某一指定站点的1,7,14,30天数据的环比
    :param station_overview_ori:
    :param choose_day:
    :param station_name:
    :return:
    """
    if (station_overview_ori is None) or (not isinstance(station_overview_ori, pd.DataFrame)):
        return

    station_overview_ori = station_overview_ori[station_overview_ori['station'] == station_name]
    if not isinstance(choose_day, int):
        choose_day = int(choose_day)
    # 计算站点的负责人
    station_manager = get_mamager_info()
    manager_name = station_manager['ad_manger'][station_manager['station'] == station_name.lower()]
    if manager_name.empty:
        manager_name = 'None'
    else:
        manager_name = manager_name.values[0]

    def calc_station_day(station_overview_ori, window):
        new_date = max(station_overview_ori['date'])
        start_date = new_date - datetime.timedelta(days=window * choose_day)
        end_date = new_date - datetime.timedelta(days=(window - 1) * choose_day)
        date_before_data = station_overview_ori[
            (station_overview_ori['date'] <= end_date) & (station_overview_ori['date'] > start_date)]
        if date_before_data is None:
            return []
        station_num = len(date_before_data)
        if station_num != choose_day:
            return []
        sum_ad_spend = int(sum(date_before_data['ad_spend']))
        sum_ad_sales = int(sum(date_before_data['ad_sales']))
        sum_shop_sales = int(sum(date_before_data['shop_sales']))
        if sum_ad_sales > 0:
            sum_acos = str(round(100 * sum_ad_spend / sum_ad_sales, 2)) + '%'
        else:
            sum_acos = '0.00%'
        if sum_shop_sales > 0:
            sum_sale_rate = str(round(100 * sum_ad_sales / sum_shop_sales, 2)) + '%'
            sum_spend_rate = str(round(100 * sum_ad_spend / sum_shop_sales, 2)) + '%'
        else:
            sum_spend_rate = '0%'
            sum_sale_rate = '0%'
        return [choose_day, sum_ad_spend, sum_ad_sales, sum_shop_sales, station_num, sum_acos, sum_sale_rate,
                sum_spend_rate]

    group_date = [1, 2, 3]
    all_days_group = [calc_station_day(station_overview_ori, window) for window in group_date]
    if all_days_group is None:
        return
    try:
        all_days_group = pd.DataFrame(all_days_group,
                                      columns=['choose_day', 'ad_spend', 'ad_sales', 'shop_sales', 'station_num',
                                               'acos',
                                               'sale_rate', 'spend_rate'])
    except Exception as e:
        return
    all_days_group['ad_manager'] = manager_name
    all_days_group['station'] = station_name
    all_days_group = all_days_group[
        ['station', 'choose_day', 'ad_manager', 'ad_spend', 'ad_sales', 'shop_sales', 'station_num', 'acos',
         'sale_rate', 'spend_rate']]
    last_day = str(max(station_overview_ori['date'].values))[5:]
    yes_day = str(max(station_overview_ori['date'].values) - datetime.timedelta(days=1))[5:]
    yes_before_day = str(max(station_overview_ori['date'].values) - datetime.timedelta(days=2))[5:]
    date_show_name = {1: [last_day, yes_day, yes_before_day], 7: ['近7天', '上个7天', '上上个7天'],
                      14: ['近14天', '上个14天', '上上个14天'], 30: ['近30天', '上个30天', '上上个30天']}
    choose_day_date_show = date_show_name[choose_day]
    all_days_group['choose_day'] = choose_day_date_show
    all_days_group.fillna(value='', inplace=True)
    all_days_group = all_days_group.applymap(lambda x: int(x) if not isinstance(x, str) else x)
    # 增加额外列
    # 广告花费、广告销售额、站点销售额、ACoS、销售占比、花费占比的环比
    # 可以新建相对应的辅助列

    return all_days_group


# 站点概览第1层级
def overview_days(request):
    """
    # 这个函数处理第一层级
    :param request:
    :return:
    """
    # session验证不通过,返回到登录界面
    if not request.session.get("is_login", None):
        return HttpResponseRedirect("/login/")
    # session验证 存在数据库中，所以要先makemigrations生成数据库
    if request.session.get("is_login", None):
        name = request.session.get("username", None)
    station_info_ori = db_download_station_overview_ori()
    all_days_info = group_all_days(station_info_ori)
    return render_to_response('overview_by_days.html', locals())


# 站点概览第2层
def overview_stations(request, choose_day):
    """
    显示某指定的天数下站点的详情
    :param request:
    :param choose_day:
    :return:
    """
    # session验证不通过,返回到登录界面
    if not request.session.get("is_login", None):
        return HttpResponseRedirect("/login/")
    # session验证 存在数据库中，所以要先makemigrations生成数据库
    if request.session.get("is_login", None):
        name = request.session.get("username", None)
    station_info_ori = db_download_station_overview_ori()
    days = [1, 7, 14, 30]
    station_overview_stations = group_all_stations(station_info_ori, choose_day)
    return render_to_response('overview_by_stations.html', locals())


# 站点概览第3层
def overview_station_day(request, station_name, choose_day):
    """
    得到指定站点指定天数的表现:
    账号，日期，广告接手人，广告花费(包含环比)，广告销售额(包含环比)，站点销售额(包含环比)，ACoS(包含环比)，销售占比(包含环比)，花费占比(包含环比)
    :param request:
    :param choose_day:指定的天数
    :param station_name:站点名
    :return:
    """
    # session验证不通过,返回到登录界面
    if not request.session.get("is_login", None):
        return HttpResponseRedirect("/login/")
    # session验证 存在数据库中，所以要先makemigrations生成数据库
    if request.session.get("is_login", None):
        name = request.session.get("username", None)
    station_info_ori = db_download_station_overview_ori()
    station_info_ori = db_download_station_overview_ori()
    days = [1, 7, 14, 30]
    station_day_info = group_station_day(station_info_ori, station_name, choose_day)
    return render_to_response('overview_by_station_days.html', locals())
