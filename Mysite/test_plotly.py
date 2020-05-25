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

# 单一数据源
x = pd.Series([1, 2, 3, 4])
y1 = pd.Series([10, 15, 13, 17])
y2 = pd.Series([8, 13, 11, 15])
""" 
1.绘制柱状图
go.Bar
"""
# trace0 = go.Bar(
#     x=x,
#     y=y1,
#     marker=dict(
#         color=["red", "blue","red", "blue"],
#     ),
#     text= y1.values,
#     textposition='outside'
# )
# # 图形的布局
# layout = go.Layout(
#     title='测试'
# )
#
# fig = go.Figure(data=trace0, layout=layout)
# plot(fig, filename='123.html')


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

# trace=go.Box(
#     x=[0.1,2,2,2,3,3,4,5,10],
#     marker=dict(
#         color='red'
#     )
#
# )
#
# data=[trace]
#
# fig= go.Figure(data=data)
# plot(fig, filename='plot_box.html')