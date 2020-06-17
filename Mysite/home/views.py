from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect, Http404, HttpResponse, render_to_response
from django_pandas.io import read_frame
from login.models import StationSalesOverall
import warnings
from datetime import datetime

import profile
import pandas as pd
from datetime import datetime
from plotly.offline import plot
import plotly.graph_objs as go
from plotly.subplots import make_subplots

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

# 绘制实验室
def my_plotly(request):
    """
        参照亚马逊广告后台可视化主函数
        步骤:
            1.从数据库中加载数据源
            2.绘制
    Returns:

    """
    # 1.数据库中加载数据源
    table_name = 'only_station_info'
    sql = "select * from {}".format(table_name)
    source_data = conn_db.read_table(sql)
    # 选择60个数据行 销售额在180-240之间的站点
    # 选择列为acos ad_sales shop_sales cpc
    choose_data = source_data.sort_values(by=['ad_sales'], ascending=False)
    choose_rows = 60
    choose_data = choose_data[['acos', 'ad_sales', 'shop_sales', 'cpc']][180:(180 + choose_rows)]
    choose_data['date'] = pd.date_range(end=datetime.now().date(), periods=choose_rows)
    # Create figure with secondary y-axis
    data_color = {'acos': '#f8a51b', 'ad_sales': '#21409a', 'shop_sales': 'green', 'cpc': 'blue'}
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    trace_acos = go.Scatter(x=choose_data['date'], y=choose_data['acos'], mode='lines', name='acos', showlegend=False,
                            line=dict(color=data_color['acos']),hovertemplate = "%{y}%")
    trace_ad_sales = go.Scatter(x=choose_data['date'], y=choose_data['ad_sales'], mode='lines', name='广告销售额',
                                showlegend=False, yaxis='y2', line=dict(color=data_color['ad_sales']),hovertemplate = "$%{y}",
                                )
    fig.update_layout(
        height=300,
        width=1200,
        font=
        dict(
            family="Courier New, monospace",
            size=12,
            color="#7f7f7f"
        ),
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=0,
            pad=0
        ),
        paper_bgcolor="white",
        plot_bgcolor='white',
        xaxis=dict(linecolor='gray', linewidth=1),
        yaxis=dict(gridcolor='rgba(0,0,0,0.2)', gridwidth=0.3, tickfont=dict(
            color=data_color['acos'])),  # 绘制第一个Y坐标轴
        yaxis2=dict(
            tickfont=dict(
                color=data_color['ad_sales']), ),
        hovermode="x unified",
        hoverlabel=dict(
            bgcolor="white",
            font_size=16,
            font_family="宋体"
        )

    )
    fig.add_trace(trace_acos, secondary_y=False)
    fig.add_trace(trace_ad_sales, secondary_y=True)
    fig.update_traces()
    # 'displayModeBar': False # 隐藏
    config = {'displayModeBar': False}
    show_plotly = plot(fig, config=config,output_type='div')
    return render_to_response('plotly.html', locals())

