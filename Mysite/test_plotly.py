# -*- coding: utf-8 -*-
"""
Proj: web_0.0
Created on:   2020/5/15 14:40
@Author: RAMSEY

Standard:  
    s: data start
    t: important  temp data
    r: result
    error1: error type1 do not have file
    error2: error type2 file empty
    error3: error type3 do not have needed data
"""

from plotly.offline import plot
import plotly.graph_objs as go
import pandas as pd
import json
import pandas as pd
from plotly.subplots import make_subplots



# 1.导入数据源
source_data = pd.read_excel(r"C:\Users\Administrator\Desktop\ceavo_es.xlsx")
# print(source_data)

# 绘制图层
acos = go.Scatter(x = source_data['日期'],y=source_data['ACOS'],name='acos',mode='lines',yaxis='y1',line=dict(color='blue'))
cpc  = go.Scatter(x = source_data['日期'],y=source_data['CPC'],name='cpc',mode='lines',yaxis='y2',line=dict(color='red'))

# 多个数据源整合
data = [acos, cpc]

# 坐标轴的样式
axis_templates = dict(
    showgrid=False,  # 网格
    zeroline=True,  # 是否显示基线,即沿着(0,0)画出x轴和y轴
    nticks=20,
    showline=True,
    linewidth=1,
    linecolor='black',
    zerolinecolor="#FF0000"
)

# 图形的布局
layout = go.Layout(
    # 显示图标名
    title='参数',
    # 图名的颜色和字体
    titlefont=dict(color='red', family='Times New Roman'),
    # 显示图例名称
    showlegend=True,
    # 显示图例的位置
    # x,y是相对于坐标轴的比例
    legend=dict(
        x=0.9,
        y=1.1
    ),
    # 设置x,y轴的样式
    xaxis=axis_templates,
    yaxis1=dict(title='Moddel Difference 1',
                showline=True,
    linewidth=0.5,
    linecolor='black',
    titlefont=dict(
            color="blue"),
    tickfont=dict(
            color="blue"),
                ),
    yaxis2=dict(title='Moddel Difference 2',
                                   overlaying='y',
                                   side='right',showline=True,
    linewidth=0.5,
    linecolor='black',
    titlefont=dict(
        color="red"),
    tickfont=dict(
        color="red"),
        ),
    # 设置画布背景颜色
    paper_bgcolor='white', # set the background colour
    # 设置图标的背景颜色
    plot_bgcolor='white'
)

# 生成一个图
fig = go.Figure(data=data, layout=layout)
# 将图绘制并输出到html中
fig.update_layout(   height=600,
    width=1800)
config = {'displayModeBar': False}
plot(fig, filename='123.html',config=config)



# # 单一数据源
# x = pd.Series([1, 2, 3, 4])
# y1 = pd.Series([10, 15, 13, 17])
# y2 = pd.Series([8, 13, 11, 15])
# """
# 1.绘制柱状图
# go.Bar
# """
# trace0 = go.Bar(
#     x=x,
#     y=y1,
#     marker=dict(
#         color=["red", "blue","red", "blue"],
#     ),
#     text= y1.values,
#     textposition='outside',
#     name= '柱状图'
# )
# trace1 = go.Scatter(
#     x=x,
#     y=y2,
#     marker=dict(
#         color=["red", "blue","red", "blue"],
#     ),
#     mode='lines',
#     name='折线图'
# )
# trace2 = go.Scatter(
#     x=x,
#     y=y1,
#     marker=dict(
#         color=["red", "blue","red", "blue"],
#     ),
#     mode='lines',
#     name='折线图'
# )
#
# # 图形的布局
# layout = go.Layout(
#     title='测试'
# )
# # config可以显示或者去掉plotly编辑框
# # 'displayModeBar': True # 显示
# # 'displayModeBar': False # 隐藏
# config = {'displayModeBar': False}
#
# fig = make_subplots(rows=1, cols=3,shared_xaxes=False,subplot_titles=("Plot 1", "Plot 2", "Plot 3"),y_title='y axis title 1')
# # config可以显示或者去掉plotly编辑框
# fig.add_trace(trace0,row=1,col=1)
# fig.add_trace(trace1,row=1,col=3)
# fig.add_trace(trace2,row=1,col=2)
#
# # 更新图层的高宽和标题
# fig.update_layout(
#     title_text="Subplot Title",
#     height=600,
#     width=1800,
#     font=dict(
#         family="Courier New, monospace",
#         size=18,
#         color="#7f7f7f"
#     )
# )
# # 修改x轴标签
# fig.update_xaxes(title_text='x axis title 1',row=1,col=1)
# fig.update_xaxes(title_text='x axis title 2',row=1,col=2)
# fig.update_xaxes(title_text='x axis title 3',row=1,col=3)
#
# plot(fig, filename='123.html',config = config )
#
#
#
# fig = go.Figure(go.Indicator(
#     mode = "gauge+number",
#     value = 270,
#     domain = {'x': [0, 1], 'y': [0, 1]},
#     title = {'text': "Speed"}))
# fig.update_layout(   height=600,
#     width=1800)
# plot(fig, filename='123.html',config = config )


"""
2.绘制散点图(详细的介绍了参数) 
go.Scatter
"""

# trace0 = go.Scatter(
#     x=x,
#     y=y1,
#     marker=dict(
#         color=["red", "blue", "red", "blue"],
#         size=[20, 30, 20, 30]
#     ),
#     text=['fuck1', 'fuck2', 'fuck3', 'fuck4'],
#     mode="markers+lines",
#     textposition='top center',
#     name='line1',
#     # 填充区域(面积图)
#     fill='tonexty',
#     # 填充颜色
#     fillcolor='green'
# )
# trace1 = go.Scatter(
#     # 数据源
#     x=x,
#     y=y2,
#     # 标记点的样式：颜色和大小
#     marker=dict(
#         color=["red", "blue", "red", "blue"],
#     ),
#     text=['fuck1', 'fuck2', 'fuck3', 'fuck4'],
#     # 散点图中数据点的展现形式,标记(markers)+线性(lines)
#     mode="markers+lines",
#     # 标记数据的数据文本展示位置
#     textposition='top center',
#     # 数据组的命名
#     name='line2',
#     # 填充区域(面积图)
#     fill='tonexty',
#     # 填充颜色
#     fillcolor='white'
# )
#
# # 多个数据源整合
# data = [trace0, trace1]
#
# # 坐标轴的样式
# axis_templates = dict(
#     showgrid=False,  # 网格
#     zeroline=False,  # 是否显示基线,即沿着(0,0)画出x轴和y轴
#     nticks=20,
#     showline=False,
#     title='X axis',# 坐标名称
#     mirror='all',
#     zerolinecolor="#FF0000"
# )
#
# # 图形的布局
# layout = go.Layout(
#     # 显示图标名
#     title='测试',
#     # 图名的颜色和字体
#     titlefont=dict(color='red', family='Times New Roman'),
#     # 显示图例名称
#     showlegend=True,
#     # 显示图例的位置
#     # x,y是相对于坐标轴的比例
#     legend=dict(
#         x=0.9,
#         y=0.9
#     ),
#     # 设置x,y轴的样式
#     xaxis=axis_templates,
#     # 设置画布背景颜色
#     paper_bgcolor='rgb(0,0,0,0.5)', # set the background colour
#     # 设置图标的背景颜色
#     plot_bgcolor='rgba(255,255,255,1)'
# )
#
# # 生成一个图
# fig = go.Figure(data=data, layout=layout)
# # 将图绘制并输出到html中
# plot(fig, filename='123.html')

"""
3.绘制频率直方图
go.Histogram
"""
# data_histogram = [1, 2, 2, 3, 3, 4, 5, 6, 7, 7, 7, 9]
#
# # 设置图形的格式
# trace0 = go.Histogram(
#     x= data_histogram,
#     marker=dict(color=['red','green','black']),
#     text=list(set(data_histogram)),
# )
# # 设置坐标轴
# axis_templates = dict(
#     title='X axis',  # 坐标名称
# )
#
# # 设置绘画框格式
# layout = dict(
#     title='histogram',
#     xaxis=axis_templates
# )
#
# data = [trace0]
# # 生成图形
# fig = go.Figure(data=data, layout=layout)
# plot(fig, filename='plot_histogram.html')

"""
4.绘制GPS点地图
go.Scattergeo
"""

# # 经纬度
# geo_lon = [114.25,112.74]
# geo_lat = [30.62,29.84]
#
# trace_geo = go.Scattergeo(
#     lon=geo_lon,
#     lat=geo_lat,
#     marker=dict(
#         color=['red','black'],
#         size=[30,20]
#     ),
#     text=['武汉','大垸']
# )
#
#
# layout=dict(
#     title='GPS',
# )
#
# data = [trace_geo]
# # 生成图形
# fig = go.Figure(data=data, layout=layout)
# plot(fig, filename='plot_histogram.html')


"""
5. 绘制城市地图
go.Choropleth
"""


"""
6.绘制箱线图
go.Box
"""
