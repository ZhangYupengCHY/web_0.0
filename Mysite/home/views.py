from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect, Http404, HttpResponse, render_to_response
from django_pandas.io import read_frame
from login.models import StationSalesOverall
import warnings
from datetime import datetime

# Create your views here.

warnings.filterwarnings(action='ignore')


def search_station(request, all_station_info):
    """
    搜索需要的站点
    :param all_station_info: 全部的站点
    :return: 筛选后的站点信息
    """
    if request.method != 'POST':
        select_station_info = all_station_info
    else:
        search_station = request.POST.get('search_station')
        select_station_info = all_station_info[all_station_info['account'].str.contains(search_station.lower())]
    return select_station_info


def home_page(request):
    # session验证不通过,返回到登录界面
    if not request.session.get("is_login", None):
        return HttpResponseRedirect("/login/")
    # session验证 存在数据库中，所以要先makemigrations生成数据库
    if request.session.get("is_login", None):
        name = request.session.get("username", None)
        now_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print('********************************************')
        print('USER: {}'.format(name))
        print('TIME: {}'.format(now_datetime))
        print('********************************************')
    station_info_temp = StationSalesOverall.objects.all()
    station_info_temp = read_frame(station_info_temp)
    station_info = station_info_temp[(station_info_temp['acos'] > 0.2) & (station_info_temp['ad_sales'] > 3000)]
    station_info[['ad_spend', 'ad_sales', 'shop_sales', 'shop_sales']] = station_info[
        ['ad_spend', 'ad_sales', 'shop_sales', 'shop_sales']].applymap(lambda x: int(x))
    station_info.sort_values(by=['ad_sales', 'acos'], ascending=False, inplace=True)
    station_info[['acos_str', 'spend_rate_str', 'sale_rate_str']] = station_info[
        ['acos', 'spend_rate', 'sale_rate']].applymap(lambda x: str(round((x * 100), 2)) + '%')
    station_info['update_datetime'] = station_info['update_datetime'].dt.strftime('%Y-%m-%d %H:%M:%S')
    select_station_info = search_station(request, station_info)
    return render_to_response('home_page.html', locals())
