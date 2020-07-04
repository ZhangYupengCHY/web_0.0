from random import randint

from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect, Http404, HttpResponse, render_to_response
from pyecharts.charts import Timeline
from require.models import Submit
from datetime import datetime
from django_pandas.io import read_frame
from plotly.offline import plot
import plotly.graph_objs as go
from pyecharts.charts.basic_charts.bar import Bar
from pyecharts import options as opts
import warnings


# Create your views here.

warnings.filterwarnings(action='ignore')

# 更新数据
def update(request):
    if request.method == 'POST':
        pk = request.POST.get('pk')
        v = request.POST.get('value')
        print(pk,v)
    return render_to_response('require.html', locals())


def plot_timeline():
    """
    Timeline可以将多个图表制作成动画。
    :return:
    """
    # 初始化多组数据
    attr = ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"]
    year = 5
    start_year = 2018
    num = len(attr)
    # 初始化时间线图形
    timeline = Timeline(init_opts=opts.InitOpts(width='120%', height='300%'))

    # 时间轴添加配置项
    timeline.add_schema(is_auto_play=False, is_loop_play=True, is_timeline_show=True, control_position='right',
                        itemstyle_opts=opts.ItemStyleOpts(color='blue', opacity=0.8),play_interval=1000)

    for i in range(5):
        year_sales1 = [randint(10, 100) for _ in range(num)]
        year_sales2 = [randint(200, 500) for _ in range(num)]
        # 初始化
        bar_temp = Bar(init_opts=opts.InitOpts())
        # 加载数据
        bar_temp.add_xaxis(xaxis_data=attr)
        bar_temp.add_yaxis(series_name=f'{start_year+i}年净销售额',y_axis=year_sales1)
        bar_temp.add_yaxis(series_name=f'{start_year+i}年实际销售额',y_axis=year_sales2)
        # bar配置项
        bar_temp.set_global_opts(title_opts=opts.TitleOpts(title=f'{start_year + i} 销售额情况'))

        # 时间轮播图添加图形
        timeline.add(bar_temp, f'{start_year + i}年营业额')

    # 输出时间线轮播图
    return timeline.render_embed()


# 获取已经提交的需求
def get_required_info():
    """
    列名: type submitter datetime status brief content
    :return:
    """
    required_temp = Submit.objects.all()
    required_info = read_frame(required_temp)
    return required_info


def require(request):
    name = request.session.get("username", None)
    required_info = get_required_info()
    if request.method != 'POST':
        pass
    else:
        require_type = request.POST.get('require_type')
        require_brief = request.POST.get('require_brief')
        require_content = request.POST.get('require_content')
        name = request.session.get("username", None)
        now_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        require_id = required_info.shape[0] + 1

        # 判断是否重复提交
        required_contents = set(required_info['content'])

        if require_content in required_contents:
            pass

        else:
            Submit.objects.create(id=require_id, type=require_type, submitter=name, datetime=now_datetime,
                                  brief=require_brief, content=require_content)
            required_info = get_required_info()

    required_info['datetime'] = required_info['datetime'].dt.strftime('%Y-%m-%d %H:%M:%S')
    timeline = plot_timeline()
    return render_to_response('require.html', locals())
