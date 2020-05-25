from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect, Http404, HttpResponse, render_to_response
from require.models import Submit
from datetime import datetime
from django_pandas.io import read_frame
from plotly.offline import plot
import plotly.graph_objs as go


# Create your views here.


def test_show():
    x_data = [0, 1, 2, 3, 4, 5, 6]
    y_data = [x ** 2 for x in x_data]
    plot_div = plot([go.Scatter(x=x_data, y=y_data, mode='lines', name='test', opacity=0.8, marker_color='green')],
                    output_type='div')
    return plot_div


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
    plt_div = test_show()
    return render_to_response('require.html', locals())
