from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect, Http404, HttpResponse, render_to_response
from django_pandas.io import read_frame
from manager_perf.models import StationSalesOverall
from manager_perf.models import OnlyStationInfo
import math


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


# 得到每个站点负责人负责的站点数
def charge_stations_num():
    manager_info = get_mamager_info()
    charge_num = manager_info[['ad_manger', 'owner']].groupby(['ad_manger']).agg({'ad_manger': 'count'})
    charge_num.index.name = 'num'
    charge_num.sort_values(by='ad_manger', ascending=False, inplace=True)
    return charge_num


# 查询站点
def search_station(request, all_station_info):
    if (request.method == 'POST') and ('search_station' in request.POST):
        search_station = request.POST.get('search_station')
        if search_station is not None:
            select_station_info = all_station_info[all_station_info['station'].str.contains(search_station.lower())]
            return select_station_info
    return all_station_info


# 页数
def data_page(data, one_page_num=10):
    """
    将数据实现分页功能
    data:
        dataframe需要实现分页的数据
    page_name:
        翻页的标签名
    one_page_num:
        一页显示多少行,默认为10行
    :return:
    """
    data_len = len(data)
    if data_len == 0:
        return
    page_num = math.ceil(data_len / one_page_num)
    page_list = list(range(1, page_num + 1))
    return page_list


# 获得某个专员的站点数据
def get_one_manager_data(manager_name):
    # 得到全部站点数据
    manager_info = get_mamager_info()
    all_manager_name = set(manager_info['ad_manger'])
    if manager_name in all_manager_name:
        one_manager_info = manager_info[manager_info['ad_manger'] == manager_name]
        return one_manager_info


# 每个人的前10站点数据
def manager_station_data(request, manager_name, current_page=1, add_page=0, init_every_page_num=10):
    # 得到全部站点数据
    current_page = int(current_page)
    charge_num = charge_stations_num()
    one_manager_info = get_one_manager_data(manager_name)
    data_len = len(one_manager_info)
    # 得到每页的数量
    if (request.method == 'POST') and ('select_page_num' in request.POST):
        every_page_num = request.POST.get('select_page_num')
        if every_page_num is not None:
            # print('every_page_num:{}'.format(every_page_num))
            if every_page_num == '全部':
                every_page_num = data_len
            else:
                every_page_num = int(every_page_num)
        else:
            every_page_num = init_every_page_num
    else:
        every_page_num = init_every_page_num

    # 搜索站点
    if (request.method == 'POST') and ('search_station' in request.POST):
        search_station = request.POST.get('search_station')
        if search_station is not None:
            one_manager_page_info = one_manager_info[one_manager_info['station'].str.contains(search_station.lower())]
            return render_to_response('manager_perf.html', locals())
    every_page_num = int(every_page_num)
    # 实现分页查询功能
    page_num = math.ceil(data_len / every_page_num)
    page_list = list(range(1, page_num + 1))
    if page_list:
        max_page = page_list[-1]

    # 分页数据
    def page_data(manager_info, every_page_num, current_page=1):
        """
        显示某页的数据
        :param data:
        :return:
        """
        if current_page <= 1:
            current_page = 1
        data = manager_info.reset_index(drop=True)
        one_page_info = data.ix[(current_page - 1) * every_page_num:(current_page * every_page_num) - 1, :]
        one_page_info.index += 1
        return one_page_info

    if add_page == 'left_page':
        current_page -= 1
    if add_page == 'right_page':
        current_page += 1
    if current_page <= 1:
        current_page = 1
    if current_page >= max_page:
        current_page = max_page

    one_manager_page_info = page_data(one_manager_info, every_page_num, current_page=current_page)

    return render_to_response('manager_perf.html', locals())


def manager_perf(request):
    charge_num = charge_stations_num()
    return render_to_response('manager_perf.html', locals())
